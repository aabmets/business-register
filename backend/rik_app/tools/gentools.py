from rik_app.models import *
from rik_app.types import PersonType
from rik_app.tools import tintools, nametools
from datetime import datetime, timedelta
from mimesis.locales import Locale
from mimesis import Finance
from dotmap import DotMap
from faker import Faker
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
def generate_tin(person: PersonType) -> str | None:
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
def generate_shareholder(equity: int) -> NaturalPerson | JudicialPerson:
    random.seed(secrets.token_bytes(32))
    return Shareholder(
        name=fake.name(),
        tin=generate_tin(PersonType.NATURAL),
        equity=equity,
        founder=True,
    )


# -------------------------------------------------------------------------------- #
def generate_company() -> Company:
    random.seed(secrets.token_bytes(32))
    data = generate_equity()
    shds: Shareholders = []
    for i in range(len(data.shares)):
        equity = data.shares[i]
        sh = generate_shareholder(equity)
        shds.append(sh)
    name = finance_data.company()
    count = nametools.get_identifier_count(name)
    name = name + ' OÜ' if not count else name
    Company.disable_date_validation()
    company = Company(
        name=name,
        tin=generate_tin(PersonType.JUDICIAL),
        equity=data.equity,
        founding_date=generate_iso_date(),
        shareholders=shds,
    )
    Company.enable_date_validation()
    return company


# -------------------------------------------------------------------------------- #
__all__ = [
    "generate_equity",
    "generate_iso_date",
    "generate_tin",
    "generate_shareholder",
    "generate_company",
]
