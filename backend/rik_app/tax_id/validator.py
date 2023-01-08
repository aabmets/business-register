from .helpers import *


# -------------------------------------------------------------------------------- #
def validate_tin(tin: str) -> bool:
    person = get_person_type_from_tin(tin)
    if person == Person.PRIVATE and not validate_tin_date(tin):
        return False
    elif person == Person.LEGAL and not validate_tin_prefix(tin):
        return False
    elif person == Person.INVALID:
        return False
    return is_valid_tin_checksum(tin)
