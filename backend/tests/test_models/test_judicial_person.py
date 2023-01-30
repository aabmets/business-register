from rik_app.models import JudicialPerson
from rik_app.rik_types import PersonType
from rik_app.utils import testutils
from pydantic import ValidationError
from dotmap import DotMap


# -------------------------------------------------------------------------------- #
def test_np_valid_values_1():
    np = JudicialPerson(
        name="Asperon OÜ",  # already valid name
        tin="16272114",  # full TIN with checksum
        equity=1,  # min allowable equity
        founder=True,
    )
    assert np.name == "Asperon OÜ"
    assert np.tin == "16272114"
    assert np.equity == 1
    assert np.founder is True
    assert np.person_type == PersonType.JUDICIAL


# -------------------------------------------------------------------------------- #
def test_np_valid_values_2():
    np = JudicialPerson(
        name="   Asperon   OÜ   ",  # string is automatically normalized
        tin="1627211",  # checksum is automatically calculated
        equity=25000,  # max allowable equity
        founder=False,
        person_type=PersonType.JUDICIAL
    )
    assert np.name == "Asperon OÜ"
    assert np.tin == "16272114"
    assert np.equity == 25000
    assert np.founder is False
    assert np.person_type == PersonType.JUDICIAL


# -------------------------------------------------------------------------------- #
def test_np_missing_values():
    try:
        JudicialPerson()
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
        DotMap(name="$$$ OÜ", err_msg="name.invalid-char-judicial"),
        DotMap(name="ABC ABC", err_msg="name.not-judicial-type"),
        DotMap(name="OÜ ABC OÜ", err_msg="name.invalid-id-count"),
        DotMap(name="Osaühing ABC osaühing", err_msg="name.invalid-id-count"),
        DotMap(name="OsaühingABC", err_msg="name.invalid-id-value"),
        DotMap(name="ABCOsaühing", err_msg="name.invalid-id-value"),
        DotMap(name="ABC OÜ DEF", err_msg="name.invalid-id-position"),
        DotMap(name="ABC Osaühing DEF", err_msg="name.invalid-id-position"),
    ]
    testutils.assert_failure(tests, JudicialPerson, tin="16272114", equity=1)


# -------------------------------------------------------------------------------- #
def test_np_tin_errors():
    tests = [
        DotMap(tin="123abc", err_msg="tin.invalid-digit"),
        DotMap(tin="123456", err_msg="tin.invalid-length"),
        DotMap(tin="123456789", err_msg="tin.invalid-length"),
        DotMap(tin="123456789012", err_msg="tin.invalid-length"),
        DotMap(tin="61104089528", err_msg="tin.not-judicial-type"),
        DotMap(tin="6110408952", err_msg="tin.not-judicial-type"),
        DotMap(tin="36272114", err_msg="tin.invalid-prefix-data"),
        DotMap(tin="96272114", err_msg="tin.invalid-prefix-data"),
        DotMap(tin="16272110", err_msg="tin.invalid-judicial-checksum"),
        DotMap(tin="16272118", err_msg="tin.invalid-judicial-checksum"),
    ]
    testutils.assert_failure(tests, JudicialPerson, name="Asperon OÜ", equity=1)


# -------------------------------------------------------------------------------- #
def test_np_equity_errors():
    tests = [
        DotMap(equity=0, err_msg="equity.too-small"),
        DotMap(equity=25001, err_msg="equity.too-large"),
    ]
    testutils.assert_failure(tests, JudicialPerson, name="Asperon OÜ", tin="16272114")
