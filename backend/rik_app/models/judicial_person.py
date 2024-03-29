from rik_app.rik_types import PersonType
from rik_app.tools import nametools
from rik_app.tools import tintools
from pydantic import validator
from .person import Person


# -------------------------------------------------------------------------------- #
class JudicialPerson(Person):
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
        self.person_type = PersonType.JUDICIAL

    # ------------------------------------------------------------ #
    @validator("name")
    def validate_judicial_name(cls, name: str) -> str:
        """
        This function validates that the name of a judicial person contains
        only one of the required identifiers and that the identifier is
        located either at the beginning or at the end of the name.

        :raises "name.not-judicial-type": if the name doesn't contain
            any identifiers at all, even invalid ones.
        :raises "name.invalid-id-count": if the name contains
            more than one identifier.
        :raises "name.invalid-id-value": if the identifier is 'osaühing'
            and it's not a separate word in the name.
        :raises "name.invalid-id-position": if the identifier is not
            at the beginning or at the end of the name.
        :param name: JudicialPerson name.
        :return: JudicialPerson name, unmodified.
        """
        _person = nametools.get_person_from_name(name)
        if _person != PersonType.JUDICIAL:
            raise ValueError("name.not-judicial-type")
        if not nametools.is_valid_id_count(name):
            raise ValueError("name.invalid-id-count")
        if not nametools.is_valid_id_value(name):
            raise ValueError("name.invalid-id-value")
        if not nametools.is_valid_id_position(name):
            raise ValueError("name.invalid-id-position")
        if not nametools.is_valid_name(name, PersonType.JUDICIAL):
            raise ValueError("name.invalid-char-judicial")
        return name

    # ------------------------------------------------------------ #
    @validator("tin")
    def validate_judicial_tin(cls, full_tin: str) -> str:
        """
        This function validates that the TIN of a JudicialPerson
        has the correct structure and contains the valid data.

        :raises "tin.not-judicial-type": if TIN has incorrect length.
        :raises "tin.invalid-prefix-data": if TIN prefix field is invalid.
        :raises "tin.invalid-judicial-checksum": if TIN checksum is invalid.
        :param full_tin: JudicialPersons TIN.
        :return: JudicialPersons TIN, unmodified.
        """
        _person = tintools.get_person_from_tin(full_tin)
        if _person != PersonType.JUDICIAL:
            raise ValueError("tin.not-judicial-type")
        if not tintools.validate_tin_prefix(full_tin):
            raise ValueError("tin.invalid-prefix-data")
        if not tintools.validate_tin_checksum(full_tin):
            raise ValueError("tin.invalid-judicial-checksum")
        return full_tin
