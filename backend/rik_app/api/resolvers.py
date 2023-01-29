from ariadne import QueryType, MutationType
from rik_app.tools import nametools, tintools
from rik_app.db import DatabaseSingleton
from rik_app.rik_types import PersonType
from dotmap import DotMap
from .helpers import *
import json


# -------------------------------------------------------------------------------- #
query = QueryType()
mutation = MutationType()
resolvers = [query, mutation]


# -------------------------------------------------------------------------------- #
@query.field("searchCompanies")
async def resolve_search_companies(_, __, pattern: str):
    if len(pattern) < 3:
        return error_message("error.search-pattern-too-short")
    if len(pattern) > 100:
        return error_message("error.search-pattern-too-long")
    is_name = nametools.is_valid_name(pattern, PersonType.JUDICIAL)
    if not is_name and not pattern.isdecimal():
        return error_message("error.invalid-search-pattern")
    db = DatabaseSingleton()
    coro = db.fuzzy_find_companies_by_name
    if not is_name:
        coro = db.fuzzy_find_companies_by_tin
    results = await coro(pattern)
    if not results:
        return error_message("error.no-search-results")
    return data_message([dict(r) for r in results])


# -------------------------------------------------------------------------------- #
@query.field("getCompanyDetails")
async def resolve_get_company_details(_, __, tin: str):
    person = tintools.get_person_from_tin(tin)
    if person != PersonType.JUDICIAL or tintools.is_partial_tin(tin):
        return error_message("error.invalid-search-tin")
    db = DatabaseSingleton()
    result = await db.get_company_details_by_tin(tin)
    if not result:
        return error_message("error.details-not-found")
    company = DotMap(dict(result))
    company.shareholders = json.loads(company.shareholders)
    company.founding_date = str(company.founding_date)
    return data_message(company.toDict())


# -------------------------------------------------------------------------------- #
@mutation.field("createCompany")
async def resolve_create_company(_, __, data: dict):
    errors = ErrorsList()
    parsed_company = process_incoming_data(
        data=data,
        errors=errors,
        validate_date=True,
        set_founders=True,
    )
    if errors:
        return errors.to_dict()
    field_id = parsed_company.field_id

    db = DatabaseSingleton()
    exists = await db.does_company_name_exist(parsed_company)
    if exists:
        errors(field_id, "name.company-already-exists")
        return errors.to_dict()

    exists = await db.does_company_tin_exist(parsed_company)
    if exists:
        errors(field_id, "tin.company-already-exists")
        return errors.to_dict()

    await db.insert_company(parsed_company)
    return {
        "result": True,
        "data": parsed_company.to_dict()
    }


# -------------------------------------------------------------------------------- #
@mutation.field("updateCompany")
async def resolve_update_company(_, __, data: dict):
    errors = ErrorsList()
    parsed_company = process_incoming_data(
        data=data,
        errors=errors,
        validate_date=False,
        set_founders=False,
    )
    if errors:
        return errors.to_dict()
    field_id = parsed_company.field_id

    db = DatabaseSingleton()
    result = await db.get_company_details_by_tin(parsed_company.tin)
    if not result:
        errors(field_id, "name.company-doesnt-exist")
        return errors.to_dict()

    db_company = DotMap(dict(result))
    if parsed_company.equity <= db_company.equity:
        errors(field_id, "equity.equity-must-increase")
        return errors.to_dict()

    parsed_shds = parsed_company.shareholders
    db_shds = json.loads(db_company.shareholders)
    for db_sh in db_shds:
        db_sh = DotMap(db_sh)
        search_result = list(filter(lambda sh: sh.tin == db_sh.tin, parsed_shds))
        if not search_result:
            errors(field_id, "shareholders.missing-shareholder")
            break
        found_sh = search_result[0]
        if found_sh.name != db_sh.name:
            errors(found_sh.field_id, "name.shareholder-name-mismatch")
            break
        elif found_sh.equity < db_sh.equity:
            errors(found_sh.field_id, "equity.shareholder-equity-decrease")
            break
        else:
            found_sh.founder = db_sh.founder
    if errors:
        return errors.to_dict()

    for parsed_sh in parsed_shds:
        if parsed_sh.founder is None:
            parsed_sh.founder = False

    await db.update_company(parsed_company)
    return {
        "result": True,
        "data": parsed_company.to_dict()
    }
