from rik_app.models import Person
from rik_app.utils import testutils
from dotmap import DotMap
import pytest


# -------------------------------------------------------------------------------- #
def test_testutils_not_callable():
    not_failure = [DotMap(name="ASD FGH", tin="12345678", equity=10000)]
    with pytest.raises(RuntimeError):
        testutils.assert_failure(not_failure, 123)


# -------------------------------------------------------------------------------- #
def test_testutils_not_failure():
    not_failure = [DotMap(name="ASD FGH", tin="12345678", equity=10000)]
    with pytest.raises(RuntimeError):
        testutils.assert_failure(not_failure, Person)


# -------------------------------------------------------------------------------- #
def test_testutils_not_singular_failure():
    not_singular_failure = [DotMap(name="#$%~^|&=", tin="0000", equity=0)]
    with pytest.raises(RuntimeError):
        testutils.assert_failure(not_singular_failure, Person)


# -------------------------------------------------------------------------------- #
def test_testutils_good_tests():
    failures = [
        DotMap(name=f"{chr(7) * 3}", tin="12345678", equity=10000, err_msg="name.non-printable-char"),
        DotMap(name="ASD FGH", tin="0000", equity=10000, err_msg="tin.invalid-length"),
        DotMap(name="ASD FGH", tin="12345678", equity=0, err_msg="equity.too-small"),
    ]
    testutils.assert_failure(failures, Person)
