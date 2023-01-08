from .helpers import *


# -------------------------------------------------------------------------------- #
def generate_tin(person: Person) -> str | None:
    if person == Person.INVALID:
        raise RuntimeError('Cannot generate a TIN for an invalid person type.')
    elif person == Person.PRIVATE:
        century, year, month, day = generate_tin_date()
        q_nums = generate_tin_queue_num(Person.PRIVATE)
        tin_data = [century, year, month, day] + q_nums
        return assemble_full_tin(tin_data)
    elif person == Person.LEGAL:
        prefix = generate_tin_prefix()
        q_nums = generate_tin_queue_num(Person.LEGAL)
        tin_data = [prefix] + q_nums
        return assemble_full_tin(tin_data)
