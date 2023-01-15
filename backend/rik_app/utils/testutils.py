from pydantic import ValidationError
from typing import Callable
from dotmap import DotMap


# -------------------------------------------------------------------------------- #
def assert_failure(tests: list[DotMap], model: Callable, **replicate):
    if not callable(model):
        raise RuntimeError("Target object not callable.")
    for test in tests:
        test.update(replicate)
        try:
            model(**test)
            raise RuntimeError("The test is not supposed to succeed!")
        except ValidationError as obj:
            errors = obj.errors()
            if not len(errors) == 1:
                raise RuntimeError("Only a single fault can be tested per each test.")
            error = errors[0]
            assert error['msg'] == test.err_msg


# -------------------------------------------------------------------------------- #
__all__ = ["assert_failure"]
