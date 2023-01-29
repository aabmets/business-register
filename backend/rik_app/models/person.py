from pydantic import BaseModel, validator
from pydantic.fields import ModelField
from rik_app.tools import tintools
from typing import Any
import re


# -------------------------------------------------------------------------------- #
class Person(BaseModel):
    """
    Pydantic object with field validations.
    Exceptions in validator methods are propagated up the execution stack
    by the @validator decorator as pydantic.ValidationError exceptions.
    """
    name: str = None
    tin: str = None
    equity: int = None
    field_id: str = None

    # ------------------------------------------------------------ #
    @validator('*', pre=True, always=True)
    def assert_not_none(cls, value: Any, field: ModelField):
        """
        This function validates that each field of a Persons object is not None.

        :raises "*.empty-not-allowed": if the field is empty,
            where * is the name of the field.
        :param value: Value of the current field being validated.
        :param field: Name of the current field being validated.
        :return: value
        """
        if field.name in ['name', 'tin', 'equity'] and value is None:
            raise TypeError(field.name + ".empty-not-allowed")
        return value

    # ------------------------------------------------------------ #
    @validator("name")
    def validate_name(cls, name: str) -> str:
        """
        This function validates that the name of a Person is at least
        3 chars and at most 100 chars long and that it contains valid
        characters. Conditionally, any excessive whitespace is removed
        before the name is returned to the caller.

        :raises "name.too-short": if name length is less than 3 characters.
        :raises "name.too-long": if name length is greater than 100 characters.
        :raises "name.invalid-character": if name contains invalid characters.
        :param name: Persons name.
        :return: Persons name, optionally modified.
        """
        if len(name) < 3:
            raise ValueError("name.too-short")
        if len(name) > 100:
            raise ValueError("name.too-long")
        for c in name:
            if not c.isprintable():
                raise ValueError("name.non-printable-char")
        return re.sub(r' +', ' ', name).strip()

    # ------------------------------------------------------------ #
    @validator("tin")
    def validate_tin(cls, any_tin: str) -> str:
        """
        This function validates that the Tax Identification Number
        of a Person contains only digits 0-9 and has valid length.
        Conditionally, partial TIN-s are assembled into full TIN-s
        before being returned to the caller.

        :raises "tin.invalid-digit": if TIN contains invalid characters.
        :raises "tin.invalid-length": if TIN has invalid length.
        :param any_tin: Persons TIN.
        :return: Persons TIN, optionally modified.
        """
        if not any_tin.isdecimal():
            raise ValueError("tin.invalid-digit")
        if not tintools.get_person_from_tin(any_tin):
            raise ValueError("tin.invalid-length")
        if tintools.is_partial_tin(any_tin):
            return tintools.assemble_full_tin(any_tin)
        return any_tin

    # ------------------------------------------------------------ #
    @validator("equity")
    def validate_equity(cls, equity: int) -> int:
        """
        This function validates that the equity of a Person
        is at least 1 units and at most 25 000 units.

        :raises "equity.too-small": if equity is less than 1.
        :raises "equity.too-large": if equity is greater than 25 000.
        :param equity: Persons equity.
        :return: Persons equity, unmodified.
        """
        if equity < 1:
            raise ValueError("equity.too-small")
        if equity > 25000:
            raise ValueError("equity.too-large")
        return equity
