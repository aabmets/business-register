from rik_app.types import PersonType
import re


# -------------------------------------------------------------------------------- #
valid_chars_extra = "()'.&/,"  # chars in mimesis data
valid_name_chars = ''.join([   # as defined by law
    "abcdefghijklmnopqrsšzžtuvwõäöüxyàáâãāăåąæćčçďđðèéê",
    "ēėëěęğģìíîīıïįķĺľļłńñňņòóôōőøœŕřŗśşßťţþùúûūůűųýÿźż-"
])


# -------------------------------------------------------------------------------- #
def is_valid_name(name: str, person: PersonType) -> bool:
    judicial = (person == PersonType.JUDICIAL)
    for c in name:
        conditions = [
            c.isspace(),
            c.lower() in valid_name_chars,
            c.lower() in valid_chars_extra if judicial else False,
        ]
        if not any(conditions):
            return False
    return True


# -------------------------------------------------------------------------------- #
def preprocess(name: str) -> (str, str):
    name = name if name.islower() else name.lower()
    words = name.split(' ')
    return name, words


# -------------------------------------------------------------------------------- #
def get_identifier_count(name: str) -> int:
    name, words = preprocess(name)
    strings = re.findall('osaühing', name)
    count1 = words.count('oü')
    count2 = len(strings)
    return count1 + count2


# -------------------------------------------------------------------------------- #
def get_identifier_value(name: str) -> str | None:
    name, words = preprocess(name)
    if words.count('osaühing'):
        return 'osaühing'
    elif words.count('oü'):
        return 'oü'
    return None


# -------------------------------------------------------------------------------- #
def get_identifier_position(name: str) -> int | None:
    name, words = preprocess(name)
    val = get_identifier_value(name)
    if val:
        if name.startswith(val):
            return 0
        elif name.endswith(val):
            return -1
    return None


# -------------------------------------------------------------------------------- #
def is_valid_id_count(name: str) -> bool:
    count = get_identifier_count(name)
    return True if count == 1 else False


# -------------------------------------------------------------------------------- #
def is_valid_id_value(name: str) -> bool:
    val = get_identifier_value(name)
    return True if val in ['osaühing', 'oü'] else False


# -------------------------------------------------------------------------------- #
def is_valid_id_position(name: str) -> bool:
    pos = get_identifier_position(name)
    return True if pos in [0, -1] else False


# -------------------------------------------------------------------------------- #
def get_person_from_name(name: str) -> PersonType | None:
    if name:
        count = get_identifier_count(name)
        if count == 0:
            return PersonType.NATURAL
        return PersonType.JUDICIAL
    return None


# -------------------------------------------------------------------------------- #
__all__ = [
    "is_valid_name",
    "preprocess",
    "get_identifier_count",
    "get_identifier_value",
    "get_identifier_position",
    "is_valid_id_count",
    "is_valid_id_value",
    "is_valid_id_position",
    "get_person_from_name",
]
