from rik_app.models import *
from pydantic import ValidationError
from datetime import datetime, date, timedelta
from rik_app.utils import testutils
from dotmap import DotMap
import pytest


# -------------------------------------------------------------------------------- #
@pytest.fixture
def baseline_data():
    return {
        "name": "Asperon OÜ",
        "tin": "16272114",
        "equity": 3000,
        "shareholders": [
            Shareholder(name="ABC DEF", tin="61104089528", equity=1000, founder=True),
            Shareholder(name="GHI JKL", tin="43804052213", equity=1000, founder=True),
            Shareholder(name="WER BNM", tin="45902167078", equity=1000, founder=True),
        ],
    }


# -------------------------------------------------------------------------------- #
def test_company_failure():
    with pytest.raises(ValidationError):
        Company()


# -------------------------------------------------------------------------------- #
def test_company_founding_date_1(baseline_data: dict):
    f_date = datetime.now().date()
    company = Company(
        founding_date=f_date,
        **baseline_data
    )
    assert isinstance(company, Company)
    assert isinstance(company.founding_date, date)
    assert company.founding_date == f_date


# -------------------------------------------------------------------------------- #
def test_company_founding_date_2(baseline_data: dict):
    f_date = str(datetime.now().date())
    company = Company(
        founding_date=f_date,
        **baseline_data
    )
    assert isinstance(company, Company)
    assert isinstance(company.founding_date, date)
    assert str(company.founding_date) == f_date


# -------------------------------------------------------------------------------- #
def test_company_founding_date_error(baseline_data: dict):
    future_not_allowed = datetime.now().date() + timedelta(days=1)
    too_far_past = datetime.now().date() - timedelta(days=31)
    tests = [
        DotMap(founding_date="ABCDEFG", err_msg="date.invalid-format"),
        DotMap(founding_date=future_not_allowed, err_msg="date.future-not-allowed"),
        DotMap(founding_date=too_far_past, err_msg="date.too-far-past"),
    ]
    testutils.assert_failure(tests, Company, **baseline_data)


# -------------------------------------------------------------------------------- #
def test_company_date_passthrough(baseline_data: dict):
    too_far_past = datetime.now().date() - timedelta(days=31)
    baseline_data["founding_date"] = too_far_past
    with pytest.raises(ValidationError):
        Company(**baseline_data)
    Company.set_date_validation(False)
    Company(**baseline_data)
    Company.enable_date_validation()


# -------------------------------------------------------------------------------- #
def test_company_shareholders_empty_list(baseline_data: dict):
    today = datetime.now().date()
    tests = [DotMap(founding_date=today, err_msg="shareholders.empty-not-allowed")]
    data1 = {**baseline_data, "shareholders": None}
    data2 = {**baseline_data, "shareholders": []}
    testutils.assert_failure(tests, Company, **data1)
    testutils.assert_failure(tests, Company, **data2)


# -------------------------------------------------------------------------------- #
def test_company_shareholders_duplicates(baseline_data: dict):
    sh = Shareholder(name="RET BSG", tin="45902167078", equity=1000)
    baseline_data["shareholders"].append(sh)
    today = datetime.now().date()
    tests = [DotMap(founding_date=today, err_msg="shareholders.duplicates-not-allowed")]
    testutils.assert_failure(tests, Company, **baseline_data)


# -------------------------------------------------------------------------------- #
def test_company_shareholders_equity_mismatch(baseline_data: dict):
    sh = Shareholder(name="FAI LURE", tin="32612095751", equity=1)
    baseline_data["shareholders"].append(sh)
    today = datetime.now().date()
    tests = [DotMap(founding_date=today, err_msg="shareholders.equity-mismatch")]
    testutils.assert_failure(tests, Company, **baseline_data)


# -------------------------------------------------------------------------------- #
def test_company_equity_too_small(baseline_data: dict):
    sh = Shareholder(name="WER BNM", tin="45902167078", equity=2499)
    today = datetime.now().date()

    baseline_data["shareholders"] = [sh]
    baseline_data["equity"] = 2499

    tests = [DotMap(founding_date=today, err_msg="equity.too-small")]
    testutils.assert_failure(tests, Company, **baseline_data)


# -------------------------------------------------------------------------------- #
def test_company_to_dict(baseline_data: dict):
    f_date = datetime.now().date()
    c_dict = Company(
        founding_date=f_date,
        **baseline_data
    ).to_dict()
    assert c_dict == {
        "name": "Asperon OÜ",
        "tin": "16272114",
        "equity": 3000,
        "founding_date": str(f_date),
        "shareholders": [
            {
                "name": "Abc Def",
                "tin": "61104089528",
                "equity": 1000,
                "founder": True
            }, {
                "name": "Ghi Jkl",
                "tin": "43804052213",
                "equity": 1000,
                "founder": True
            }, {
                "name": "Wer Bnm",
                "tin": "45902167078",
                "equity": 1000,
                "founder": True,
            }
        ],
    }


# -------------------------------------------------------------------------------- #
def test_company_to_dotmap(baseline_data: dict):
    f_date = datetime.now().date()
    c_dm = Company(
        founding_date=f_date,
        **baseline_data
    ).to_dotmap()
    assert isinstance(c_dm, DotMap)
