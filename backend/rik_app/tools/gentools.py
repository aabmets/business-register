from rik_app.types import *
from rik_app.models import *
from rik_app.tools import tintools, nametools
from datetime import datetime, timedelta
from mimesis.locales import Locale
from mimesis import Finance
from dotmap import DotMap
from faker import Faker
from typing import Any
import secrets
import random


# -------------------------------------------------------------------------------- #
# As globals to prevent reloading datafiles on each function call.
finance_data = Finance(locale=Locale.ET)
fake = Faker(locale="et_EE")


# -------------------------------------------------------------------------------- #
def generate_equity() -> DotMap:
    equity = random.randrange(2500, 25001)
    remainder = equity % 100
    parts = random.randint(1, 5)
    divisor = (equity - remainder) // 100
    shares = [0] * parts
    for _ in range(divisor):
        index = random.randint(0, parts - 1)
        shares[index] += 100
    shares[0] += remainder
    return DotMap(
        equity=equity,  # int
        shares=shares,  # list[int]
    )


# -------------------------------------------------------------------------------- #
def generate_iso_date() -> str:
    days = random.randrange(365 * 50)
    delta = timedelta(days=days)
    now = datetime.now().date()
    return str(now - delta)


# -------------------------------------------------------------------------------- #
def generate_tin(person: PersonType | Any) -> str:
    if person == PersonType.NATURAL:
        century, year, month, day = tintools.generate_tin_date()
        q_nums = tintools.generate_tin_queue_num(person)
        tin_data = [century, year, month, day] + q_nums
        return tintools.assemble_full_tin(tin_data)
    elif person == PersonType.JUDICIAL:
        prefix = tintools.generate_tin_prefix()
        q_nums = tintools.generate_tin_queue_num(person)
        tin_data = [prefix] + q_nums
        return tintools.assemble_full_tin(tin_data)
    raise TypeError("Cannot generate a TIN on invalid person.")


# -------------------------------------------------------------------------------- #
def generate_judicial_name() -> str:
    name = finance_data.company()
    id_count = nametools.get_identifier_count(name)
    if id_count == 1:
        pos = nametools.get_identifier_position(name)
        if pos in [0, -1]:
            _id = nametools.get_identifier_value(name)
            name_arr = name.split()
            for word in name_arr[:]:
                if word.lower() == _id:
                    name_arr.remove(word)
            name = ' '.join(name_arr)
        else:  # pragma: no cover
            return generate_judicial_name()
    elif id_count > 1:  # pragma: no cover
        return generate_judicial_name()
    return name + ' OÜ'


# -------------------------------------------------------------------------------- #
def generate_shareholder(equity: int, founder: bool) -> NaturalPerson | JudicialPerson:
    random.seed(secrets.token_bytes(32))
    tin = generate_tin(PersonType.NATURAL)
    index = int(tin[0]) % 2  # 0 = female, 1 = male
    name_func = [
        fake.name_female,
        fake.name_male
    ][index]
    return Shareholder(
        name=name_func(),
        tin=tin,
        equity=equity,
        founder=founder,
    )


# -------------------------------------------------------------------------------- #
def generate_company_names(count: int) -> list:
    names = []
    clamped_count = min(max(count, 0), 300)
    while clamped_count != 0:
        name = generate_judicial_name()
        if name not in names:
            names.append(name)
            clamped_count -= 1
    return names


# -------------------------------------------------------------------------------- #
def generate_company_tins(count: int) -> list:
    tins = []
    clamped_count = min(max(count, 0), 300)
    while clamped_count != 0:
        tin = generate_tin(PersonType.JUDICIAL)
        if tin not in tins:  # pragma: no branch
            tins.append(tin)
            clamped_count -= 1
    return tins


# -------------------------------------------------------------------------------- #
def generate_company(name: str, tin: str) -> Company:
    random.seed(secrets.token_bytes(32))
    data = generate_equity()
    shds: Shareholders = []
    for i in range(len(data.shares)):
        equity = data.shares[i]
        if len(shds) == 0:
            founder = True
        else:
            founder = random.choices(
                [True, False],
                weights=[3, 1]
            )[0]
        sh = generate_shareholder(equity, founder)
        shds.append(sh)
    date = generate_iso_date()
    Company.set_date_validation(False)
    company = Company(
        name=name,
        tin=tin,
        equity=data.equity,
        founding_date=date,
        shareholders=shds,
    )
    Company.enable_date_validation()
    return company


# -------------------------------------------------------------------------------- #
def generate_companies(count: int) -> list[Company]:
    names = generate_company_names(count)
    tins = generate_company_tins(count)
    companies = []
    for _ in range(count):
        company = generate_company(
            name=names.pop(),
            tin=tins.pop()
        )
        companies.append(company)
    return companies


# -------------------------------------------------------------------------------- #
__all__ = [
    "generate_equity",
    "generate_iso_date",
    "generate_tin",
    "generate_judicial_name",
    "generate_shareholder",
    "generate_company_names",
    "generate_company_tins",
    "generate_company",
    "generate_companies"
]
