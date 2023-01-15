from rik_app.models import Person
from rik_app.utils import testutils
from pydantic import ValidationError
from dotmap import DotMap


# -------------------------------------------------------------------------------- #
def test_person_valid_values_1():
    sh = Person(
        name="First Middle Last",  # already valid name
        tin="61104089528",  # full TIN with checksum
        equity=1,  # min allowable equity
    )
    assert sh.name == "First Middle Last"
    assert sh.tin == "61104089528"
    assert sh.equity == 1


# -------------------------------------------------------------------------------- #
def test_person_valid_values_2():
    sh = Person(
        name="  First  Middle  Last  ",  # excessive whitespace is removed
        tin="4600201574",  # checksum is automatically calculated
        equity=25000,  # max allowable equity
    )
    assert sh.name == "First Middle Last"
    assert sh.tin == "46002015748"
    assert sh.equity == 25000


# -------------------------------------------------------------------------------- #
def test_person_missing_values():
    try:
        Person()
        raise ValueError("The test is not supposed to succeed!")
    except ValidationError as obj:
        errors_list = obj.errors()
        for e in errors_list:
            assert {
                "name": "name.empty-not-allowed",
                "tin": "tin.empty-not-allowed",
                "equity": "equity.empty-not-allowed",
            }[e['loc'][0]] == e['msg']


# -------------------------------------------------------------------------------- #
def test_person_name_errors():
    tests = [
        DotMap(name="AA", err_msg="name.too-short"),
        DotMap(name=(101*'A'), err_msg="name.too-long"),
        DotMap(name=f"{chr(7) * 3}", err_msg="name.non-printable-char"),
    ]
    testutils.assert_failure(tests, Person, tin="51908094712", equity=1)


# -------------------------------------------------------------------------------- #
def test_person_tin_errors():
    tests = [
        DotMap(tin="123abc", err_msg="tin.invalid-digit"),
        DotMap(tin="123456", err_msg="tin.invalid-length"),
        DotMap(tin="123456789", err_msg="tin.invalid-length"),
        DotMap(tin="123456789012", err_msg="tin.invalid-length"),
    ]
    testutils.assert_failure(tests, Person, name="ABC DEF", equity=1)


# -------------------------------------------------------------------------------- #
def test_person_equity_errors():
    tests = [
        DotMap(equity=0, err_msg="equity.too-small"),
        DotMap(equity=25001, err_msg="equity.too-large"),
    ]
    testutils.assert_failure(tests, Person, name="ABC DEF", tin="51908094712")
