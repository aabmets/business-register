from rik_app.models import *
from rik_app.types import PersonType
from pydantic import ValidationError
import pytest


# -------------------------------------------------------------------------------- #
def test_shareholder_failure():
    with pytest.raises(ValidationError):
        Shareholder()


# -------------------------------------------------------------------------------- #
def test_shareholder_natural_person():
    sh = Shareholder(name="ABC DEF", tin="61104089528", equity=1)
    assert isinstance(sh, NaturalPerson)
    assert sh.person_type == PersonType.NATURAL


# -------------------------------------------------------------------------------- #
def test_shareholder_judicial_person():
    sh = Shareholder(name="ABC DEF Osaühing", tin="16272114", equity=1)
    assert isinstance(sh, JudicialPerson)
    assert sh.person_type == PersonType.JUDICIAL
