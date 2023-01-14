from rik_app.models import Person, NaturalPerson, JudicialPerson
from pydantic import ValidationError
from dotmap import DotMap


# -------------------------------------------------------------------------------- #
Persons = Person | NaturalPerson | JudicialPerson


# -------------------------------------------------------------------------------- #
def assert_failure(tests: list[DotMap], person: Persons, **replicate):
    if not callable(person):
        raise RuntimeError("Target object not callable.")
    for test in tests:
        test.update(replicate)
        try:
            person(**test)
            raise RuntimeError("The test is not supposed to succeed!")
        except ValidationError as obj:
            errors = obj.errors()
            if not len(errors) == 1:
                raise RuntimeError("Only a single fault can be tested per each test.")
            error = errors[0]
            assert error['msg'] == test.err_msg


# -------------------------------------------------------------------------------- #
__all__ = ["assert_failure"]
