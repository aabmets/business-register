from rik_app.models import *
from rik_app.rik_types import PersonType
from rik_app.utils import testutils
from pydantic import ValidationError
from dotmap import DotMap


# -------------------------------------------------------------------------------- #
def test_np_valid_values_1():
    np = NaturalPerson(
        name="First Middle Last",  # already valid name
        tin="61104089528",  # full TIN with checksum
        equity=1,  # min allowable equity
        founder=True,
    )
    assert np.name == "First Middle Last"
    assert np.tin == "61104089528"
    assert np.equity == 1
    assert np.founder is True
    assert np.person_type == PersonType.NATURAL


# -------------------------------------------------------------------------------- #
def test_np_valid_values_2():
    np = NaturalPerson(
        name="  FIRST  MIDDLE  LAST  ",  # string is automatically normalized
        tin="4600201574",  # checksum is automatically calculated
        equity=25000,  # max allowable equity
        founder=False,
    )
    assert np.name == "First Middle Last"
    assert np.tin == "46002015748"
    assert np.equity == 25000
    assert np.founder is False
    assert np.person_type == PersonType.NATURAL


# -------------------------------------------------------------------------------- #
def test_np_missing_values():
    try:
        NaturalPerson()
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
def test_np_name_errors():
    tests = [
        DotMap(name="AA", err_msg="name.too-short"),
        DotMap(name=(101 * 'A'), err_msg="name.too-long"),
        DotMap(name="(name)", err_msg="name.invalid-char-natural"),
        DotMap(name="ABC OÜ", err_msg="name.not-natural-type"),
        DotMap(name="OsaühingABC", err_msg="name.not-natural-type"),
        DotMap(name="Osaühing ABC", err_msg="name.not-natural-type"),
        DotMap(name="ABC", err_msg="name.not-full-natural"),
    ]
    testutils.assert_failure(tests, NaturalPerson, tin="51908094712", equity=1)


# -------------------------------------------------------------------------------- #
def test_np_tin_errors():
    tests = [
        DotMap(tin="123abc", err_msg="tin.invalid-digit"),
        DotMap(tin="123456", err_msg="tin.invalid-length"),
        DotMap(tin="123456789", err_msg="tin.invalid-length"),
        DotMap(tin="123456789012", err_msg="tin.invalid-length"),
        DotMap(tin="17746844", err_msg="tin.not-natural-type"),
        DotMap(tin="1774684", err_msg="tin.not-natural-type"),
        DotMap(tin="91908094712", err_msg="tin.invalid-date-data"),
        DotMap(tin="51961614712", err_msg="tin.invalid-date-data"),
        DotMap(tin="51908095552", err_msg="tin.invalid-checksum"),
        DotMap(tin="51908094718", err_msg="tin.invalid-checksum"),
    ]
    testutils.assert_failure(tests, NaturalPerson, name="ABC DEF", equity=1)


# -------------------------------------------------------------------------------- #
def test_np_equity_errors():
    tests = [
        DotMap(equity=0, err_msg="equity.too-small"),
        DotMap(equity=25001, err_msg="equity.too-large"),
    ]
    testutils.assert_failure(tests, NaturalPerson, name="ABC DEF", tin="51908094712")
