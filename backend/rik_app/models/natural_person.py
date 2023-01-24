from rik_app.types import PersonType
from rik_app.tools import nametools
from rik_app.tools import tintools
from pydantic import validator
from .person import Person


# -------------------------------------------------------------------------------- #
class NaturalPerson(Person):
    """
    Pydantic object with field validations.
    Exceptions in validator methods are propagated up the execution stack
    by the @validator decorator as pydantic.ValidationError exceptions.
    """
    founder: bool = None  # assigned by caller
    person_type: PersonType = None  # assigned by self

    # ------------------------------------------------------------ #
    def __init__(self, **kwargs):
        kwargs.pop("person_type", None)
        super().__init__(**kwargs)
        self.person_type = PersonType.NATURAL

    # ------------------------------------------------------------ #
    @validator("name")
    def validate_natural_name(cls, name: str) -> str:
        """
        This function validates that the name of a natural person has
        a surname and does not contain any judicial person identifiers.
        Conditionally, the words in the name are capitalized before
        the name is returned to the caller.

        :raises "name.not-natural-type": if the name contains company identifiers.
        :raises "name.not-full-natural": if the name does not have a surname.
        :param name: NaturalPersons name.
        :return: NaturalPersons name, optionally modified.
        """
        _person = nametools.get_person_from_name(name)
        if _person != PersonType.NATURAL:
            raise ValueError("name.not-natural-type")
        if not nametools.is_valid_name(name, PersonType.NATURAL):
            raise ValueError("name.invalid-char-natural")
        if name.count(' ') == 0:
            raise ValueError("name.not-full-natural")
        name = [w.capitalize() for w in name.split(' ')]
        return ' '.join(name)

    # ------------------------------------------------------------ #
    @validator("tin")
    def validate_natural_tin(cls, full_tin: str) -> str:
        """
        This function validates that the TIN of a NaturalPerson
        has the correct structure and contains the valid data.

        :raises "tin.not-natural-type": if TIN has incorrect length.
        :raises "tin.invalid-date-data": if TIN date field is invalid.
        :raises "tin.invalid-checksum": if TIN checksum is invalid.
        :param full_tin: NaturalPersons TIN.
        :return: NaturalPersons TIN, unmodified.
        """
        _person = tintools.get_person_from_tin(full_tin)
        if _person != PersonType.NATURAL:
            raise ValueError("tin.not-natural-type")
        if not tintools.validate_tin_date(full_tin):
            raise ValueError("tin.invalid-date-data")
        if not tintools.validate_tin_checksum(full_tin):
            raise ValueError("tin.invalid-checksum")
        return full_tin
