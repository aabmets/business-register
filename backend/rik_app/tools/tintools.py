from rik_app.rik_types import *
from datetime import datetime
from itertools import cycle
import calendar
import secrets


# -------------------------------------------------------------------------------- #
Input = list[int | str] | str


# -------------------------------------------------------------------------------- #
def is_full_tin(tin: str) -> bool:
    f_enums = [TINLength.FULL_NATURAL, TINLength.FULL_JUDICIAL]
    return len(tin) in [e.value for e in f_enums]


# -------------------------------------------------------------------------------- #
def is_partial_tin(tin: str) -> bool:
    p_enums = [TINLength.PARTIAL_NATURAL, TINLength.PARTIAL_JUDICIAL]
    return len(tin) in [e.value for e in p_enums]


# -------------------------------------------------------------------------------- #
def generate_tin_date() -> list[str]:
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
    return [str(century), year, month, day]


# -------------------------------------------------------------------------------- #
def validate_tin_date(np_tin: str) -> bool:
    century, year, month, day = np_tin[0], np_tin[1:3], np_tin[3:5], np_tin[5:7]
    if century in ['0', '7', '8', '9']:
        return False
    prefix = {
        century in ['1', '2']: '18',
        century in ['3', '4']: '19',
        century in ['5', '6']: '20'
    }[True]
    full_year = prefix + year
    date = full_year + '-' + month + '-' + day
    try:
        dt = datetime.fromisoformat(date)
        return dt <= datetime.now()
    except ValueError:
        return False


# -------------------------------------------------------------------------------- #
def generate_tin_prefix() -> int:
    return secrets.choice(range(10, 20))


# -------------------------------------------------------------------------------- #
def validate_tin_prefix(jp_tin: str) -> bool:
    prefix = int(jp_tin[0:2])
    if prefix in range(10, 20):
        return True
    return False


# -------------------------------------------------------------------------------- #
def generate_tin_queue_num(person: PersonType) -> list[int]:
    count: int = {
        PersonType.NATURAL: 3,
        PersonType.JUDICIAL: 5
    }[person]
    choices = list(range(0, 10))
    q_num: list[int] = []
    for _ in range(count):
        v = secrets.choice(choices)
        q_num.append(v)
    return q_num


# -------------------------------------------------------------------------------- #
def generate_tin_checksum(partial_tin: str) -> int:
    partial_tin = [int(c) for c in partial_tin]
    cycler = cycle([i for i in range(1, 10)])
    w_vals = [x for x in map(lambda x: x * next(cycler), partial_tin)]
    c_val = sum(w_vals) % 11
    if c_val == 10:
        cycler = cycle([i for i in range(3, 10)] + [1, 2])
        w_vals = [x for x in map(lambda x: x * next(cycler), partial_tin)]
        c_val = sum(w_vals) % 11
    return c_val if c_val < 10 else 0


# -------------------------------------------------------------------------------- #
def validate_tin_checksum(full_tin: Input) -> bool:
    if not is_full_tin(full_tin):
        return False
    if not isinstance(full_tin, str):
        full_tin = ''.join([str(x) for x in full_tin])
    last_idx = len(full_tin) - 1
    checksum = int(full_tin[last_idx])
    partial_tin = full_tin[0:last_idx]
    computed = generate_tin_checksum(partial_tin)
    return computed == checksum


# -------------------------------------------------------------------------------- #
def assemble_full_tin(partial1: Input, partial2: Input = None) -> str:
    if not isinstance(partial1, str):
        partial1 = ''.join([str(x) for x in partial1])
    if partial2 and not isinstance(partial2, str):
        partial2 = ''.join([str(x) for x in partial2])
    partial_tin = (partial1 + partial2) if partial2 else partial1
    checksum = generate_tin_checksum(partial_tin)
    full_tin = partial_tin + str(checksum)
    return full_tin


# -------------------------------------------------------------------------------- #
def get_person_from_tin(tin: str) -> PersonType | None:
    if tin and tin.isdecimal():
        n_enums = [TINLength.FULL_NATURAL, TINLength.PARTIAL_NATURAL]
        j_enums = [TINLength.FULL_JUDICIAL, TINLength.PARTIAL_JUDICIAL]
        if len(tin) in [e.value for e in n_enums]:
            return PersonType.NATURAL
        elif len(tin) in [e.value for e in j_enums]:
            return PersonType.JUDICIAL
    return None


# -------------------------------------------------------------------------------- #
__all__ = [
    "is_full_tin", "is_partial_tin",
    "generate_tin_date", "validate_tin_date",
    "generate_tin_prefix", "validate_tin_prefix",
    "generate_tin_checksum", "validate_tin_checksum",
    "generate_tin_queue_num", "assemble_full_tin",
    "get_person_from_tin",
]
