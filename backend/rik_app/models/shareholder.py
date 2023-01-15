from .judicial_person import JudicialPerson
from .natural_person import NaturalPerson
from rik_app.types import PersonType
from rik_app.tools import nametools


# -------------------------------------------------------------------------------- #
Shareholders = list[NaturalPerson | JudicialPerson]


# -------------------------------------------------------------------------------- #
class Shareholder:
    def __new__(cls, **data) -> NaturalPerson | JudicialPerson:
        person = nametools.get_person_from_name(data.get("name", ""))
        if person == PersonType.NATURAL:
            return NaturalPerson(**data)
        return JudicialPerson(**data)


# -------------------------------------------------------------------------------- #
__all__ = ["Shareholders", "Shareholder"]
