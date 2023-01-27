from ariadne import QueryType, MutationType
from rik_app.tools import nametools, tintools
from rik_app.db import DatabaseSingleton
from rik_app.types import PersonType
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
    valid_company = process_incoming_data(
        data=data,
        errors=errors,
        validate_date=True,
        set_founders=True,
    )
    if errors:
        return errors.to_dict()

    db = DatabaseSingleton()
    await db.insert_company(valid_company)
    return {
        "result": True,
        "data": valid_company.to_dict()
    }


# -------------------------------------------------------------------------------- #
@mutation.field("updateCompany")
async def resolve_update_company(_, __, data: dict):
    errors = ErrorsList()
    valid_company = process_incoming_data(
        data=data,
        errors=errors,
        validate_date=False,
        set_founders=False,
    )
    if errors:
        return errors.to_dict()

    db = DatabaseSingleton()
    result = await db.get_company_details_by_tin(valid_company.tin)
    if not result:
        errors("company", "error.invalid-update-target")
        return errors.to_dict()

    db_company = DotMap(dict(result))
    if valid_company.equity <= db_company.equity:
        errors("company", "error.equity-must-increase")
        return errors.to_dict()

    valid_shds = valid_company.shareholders
    db_shds = json.loads(db_company.shareholders)
    for db_sh in db_shds:
        db_sh = DotMap(db_sh)
        matched_sh = list(filter(lambda sh: sh.tin == db_sh.tin, valid_shds))
        if not matched_sh:
            errors("shareholder", "error.shareholder-missing")
            break
        matched_sh = matched_sh[0]
        if matched_sh.name != db_sh.name:
            errors("shareholder", "error.shareholder-name-mismatch")
            break
        elif matched_sh.equity < db_sh.equity:
            errors("shareholder", "error.shareholder-equity-decrease")
            break
        else:
            matched_sh.founder = db_sh.founder
    if errors:
        return errors.to_dict()

    for valid_sh in valid_shds:
        if valid_sh.founder is None:
            valid_sh.founder = False
    await db.update_company(valid_company)
    return {
        "result": True,
        "data": valid_company.to_dict()
    }
