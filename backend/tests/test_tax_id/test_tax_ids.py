from rik_app.tax_id.generator import *
from rik_app.tax_id.validator import *
import pytest


# -------------------------------------------------------------------------------- #
def test_generator_error():
    with pytest.raises(RuntimeError):
        generate_tin(Person.INVALID)


# -------------------------------------------------------------------------------- #
def test_validate_private_person_tin():
    for _ in range(100):
        tin = generate_tin(Person.PRIVATE)
        if not validate_tin(tin):
            print('Invalid TIN generated: ' + tin)
            raise RuntimeError


# -------------------------------------------------------------------------------- #
def test_validate_legal_person_tin():
    for _ in range(100):
        tin = generate_tin(Person.LEGAL)
        if not validate_tin(tin):
            print('Invalid TIN generated: ' + tin)
            raise RuntimeError
