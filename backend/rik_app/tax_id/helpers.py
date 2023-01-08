from datetime import datetime
from itertools import cycle
from enum import Enum
import calendar
import secrets


# Estonian TIN Specification
# PP = Private Person, LP = Legal Person
# -------------------------------------------------------------------------------- #
PP_FULL_TIN_LEN = 11
PP_PARTIAL_TIN_LEN = 10

LP_FULL_TIN_LEN = 8
LP_PARTIAL_TIN_LEN = 7


# -------------------------------------------------------------------------------- #
class Person(Enum):
    INVALID = 'invalid'
    PRIVATE = 'private'
    LEGAL = 'legal'


# -------------------------------------------------------------------------------- #
def get_person_type_from_tin(tin: str) -> Person:
    if len(tin) in [PP_FULL_TIN_LEN, PP_PARTIAL_TIN_LEN]:
        return Person.PRIVATE
    elif len(tin) in [LP_FULL_TIN_LEN, LP_PARTIAL_TIN_LEN]:
        return Person.LEGAL
    return Person.INVALID


# -------------------------------------------------------------------------------- #
def generate_tin_queue_num(person: Person) -> list[int] | None:
    if person == Person.INVALID:
        raise RuntimeError('Cannot generate a TIN queue number for an invalid person type.')
    count: int = {Person.PRIVATE: 3, Person.LEGAL: 5}[person]
    q_num: list[int] = []
    for _ in range(count):
        q_num.append(secrets.choice(range(1, 10)))
    return q_num


# -------------------------------------------------------------------------------- #
def generate_tin_date() -> list[int, str, int, int]:
    century = secrets.choice(range(3, 7))
    if century in [3, 4]:
        year = secrets.choice(range(1900, 1999))
    else:  # 5, 6
        year_limit = datetime.now().year + 1
        year = secrets.choice(range(2000, year_limit))
    now = datetime.now()
    if year == now.year:
        month = secrets.choice(range(1, now.month + 1))
    else:
        month = secrets.choice(range(1, 13))
    if year == now.year and month == now.month:
        day = secrets.choice(range(1, now.day + 1))
    else:
        day_limit = calendar.monthrange(year, month)[1] + 1
        day = secrets.choice(range(1, day_limit))
    year = str(year)[2:]
    month = '0' + str(month) if month < 10 else str(month)
    day = '0' + str(day) if day < 10 else str(day)
    return [century, year, month, day]


# -------------------------------------------------------------------------------- #
def validate_tin_date(tin: str) -> bool:
    century, year, month, day = tin[0], tin[1:3], tin[3:5], tin[5:7]
    if century == 0:
        return False
    prefix = {
        century in ['1', '2']: '18',
        century in ['3', '4']: '19',
        century in ['5', '6']: '20'
    }[True]
    full_year = prefix + year
    date = full_year + '/' + month + '/' + day
    try:
        dt = datetime.strptime(date, '%Y/%m/%d')
        return dt <= datetime.now()
    except ValueError:
        return False


# -------------------------------------------------------------------------------- #
def generate_tin_prefix() -> int:
    return secrets.choice(range(10, 20))


# -------------------------------------------------------------------------------- #
def validate_tin_prefix(tin: str) -> bool:
    prefix = int(tin[0:2])
    if prefix in range(10, 20):
        return True
    return False


# -------------------------------------------------------------------------------- #
def compute_tin_checksum(tin_data: str) -> int:
    tin_data = [int(c) for c in tin_data]
    cycler = cycle([i for i in range(1, 10)])
    w_vals = [x for x in map(lambda x: x * next(cycler), tin_data)]
    c_val = sum(w_vals) % 11
    if c_val == 10:
        cycler = cycle([i for i in range(3, 10)] + [1, 2])
        w_vals = [x for x in map(lambda x: x * next(cycler), tin_data)]
        c_val = sum(w_vals) % 11
    return c_val if c_val < 10 else 0


# -------------------------------------------------------------------------------- #
def is_valid_tin_checksum(tin: str | list[int]) -> bool:
    if len(tin) in [PP_FULL_TIN_LEN, LP_FULL_TIN_LEN]:
        last_idx = len(tin) - 1
        tin_data = tin[0:last_idx]
        checksum = int(tin[last_idx])
        computed = compute_tin_checksum(tin_data)
        return computed == checksum
    return False


# -------------------------------------------------------------------------------- #
def assemble_full_tin(tin_data: list[int | str]) -> str:
    tin_data = ''.join([str(x) for x in tin_data])
    checksum = compute_tin_checksum(tin_data)
    tin = tin_data + str(checksum)
    return tin
