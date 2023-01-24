from .natural_person import NaturalPerson
from .judicial_person import JudicialPerson
from rik_app.types import PersonType
from rik_app.tools import nametools


# -------------------------------------------------------------------------------- #
Shareholders = list[NaturalPerson | JudicialPerson]


# -------------------------------------------------------------------------------- #
class Shareholder:
    """
    This is a helper class which automatically instantiates the correct
    Person subclass depending on the value of the name field when called.
    """
    # ------------------------------------------------------------ #
    def __new__(cls, **data) -> NaturalPerson | JudicialPerson:
        person = nametools.get_person_from_name(data.get("name", ""))
        if person == PersonType.NATURAL:
            return NaturalPerson(**data)
        return JudicialPerson(**data)


# -------------------------------------------------------------------------------- #
__all__ = ["Shareholders", "Shareholder"]
