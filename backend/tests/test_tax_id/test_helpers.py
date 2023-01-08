from rik_app.tax_id.helpers import *
import pytest


# -------------------------------------------------------------------------------- #
def test_get_person_type_from_tin():
    assert get_person_type_from_tin('1234567890') == Person.PRIVATE
    assert get_person_type_from_tin('12345678901') == Person.PRIVATE
    assert get_person_type_from_tin('1234567') == Person.LEGAL
    assert get_person_type_from_tin('12345678') == Person.LEGAL
    assert get_person_type_from_tin('123456') == Person.INVALID
    assert get_person_type_from_tin('123456789') == Person.INVALID
    assert get_person_type_from_tin('123456789012') == Person.INVALID


# -------------------------------------------------------------------------------- #
def test_generate_tin_queue_num():
    with pytest.raises(RuntimeError):
        generate_tin_queue_num(Person.INVALID)
    q_num = generate_tin_queue_num(Person.PRIVATE)
    assert len(q_num) == 3
    for i in q_num:
        assert i < 10
        assert isinstance(i, int)
    q_num = generate_tin_queue_num(Person.LEGAL)
    assert len(q_num) == 5
    for i in q_num:
        assert i < 10
        assert isinstance(i, int)


# -------------------------------------------------------------------------------- #
def test_tin_date():
    for _ in range(100):
        tin = generate_tin_date()
        tin = ''.join([str(x) for x in tin])
        if not validate_tin_date(tin):
            print(tin)
            raise ValueError('Invalid TIN date generated.')


# -------------------------------------------------------------------------------- #
def test_tin_prefix():
    for _ in range(10):
        prefix = generate_tin_prefix()
        if not validate_tin_prefix(str(prefix)):
            raise ValueError('Invalid TIN prefix generated.')


# -------------------------------------------------------------------------------- #
def test_tin_checksum():
    tins = [
        '52107045790', '35801045273', '43312064989',
        '34311134948', '37901164727', '46002015748',
        '43001135267', '43909135791', '43107222710',
        '32706149555', '42502274964', '62002230151',
        '60706060153', '35109230115', '32612095751',
        '44001102736', '51006286021', '33407152276',
        '43804052213', '61104089528', '32411020129',
        '46306122777', '36102264789', '42509072227',
        '47201104742', '32404154297', '51908094712',
        '34310014204', '49801027044', '50409136572',
        '45902167078', '51206175224', '45603126506'
    ]
    for tin in tins:
        assert is_valid_tin_checksum(tin)


# -------------------------------------------------------------------------------- #
def test_assemble_full_tin():
    tin = assemble_full_tin([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
    assert isinstance(tin, str)
    assert len(tin) == 11
    tin = assemble_full_tin([1, 2, 3, 4, 5, 6, 7])
    assert len(tin) == 8
