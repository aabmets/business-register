from rik_app.tools import tintools
from rik_app.types import *


# -------------------------------------------------------------------------------- #
def test_is_full_tin():
    for x in range(1, 20):
        result = tintools.is_full_tin('0' * x)
        assert result if x in [8, 11] else not result


# -------------------------------------------------------------------------------- #
def test_is_partial_tin():
    for x in range(1, 20):
        result = tintools.is_partial_tin('0' * x)
        assert result if x in [7, 10] else not result


# -------------------------------------------------------------------------------- #
def test_generate_tin_queue_num():
    q_num = tintools.generate_tin_queue_num(PersonType.NATURAL)
    assert len(q_num) == 3
    for i in q_num:
        assert i < 10
        assert isinstance(i, int)
    q_num = tintools.generate_tin_queue_num(PersonType.JUDICIAL)
    assert len(q_num) == 5
    for i in q_num:
        assert i < 10
        assert isinstance(i, int)


# -------------------------------------------------------------------------------- #
def test_validate_tin_date_success():
    for _ in range(1000):
        date = tintools.generate_tin_date()
        date = ''.join([str(x) for x in date])
        if not tintools.validate_tin_date(date):  # pragma: no cover
            raise ValueError('Invalid TIN date generated: ' + date)


# -------------------------------------------------------------------------------- #
def test_validate_tin_date_failure():
    for i in range(0, 10):
        assert not tintools.validate_tin_date(str(i) + '0987654321')


# -------------------------------------------------------------------------------- #
def test_generate_tin_prefix():
    for _ in range(100):
        pfs = list(range(10, 20))
        pf = tintools.generate_tin_prefix()
        assert pf in pfs


# -------------------------------------------------------------------------------- #
def test_validate_tin_prefix_success():
    for i in range(10, 20):
        assert tintools.validate_tin_prefix(str(i) + '0000')


# -------------------------------------------------------------------------------- #
def test_validate_tin_prefix_failure():
    for i in range(0, 9):
        assert not tintools.validate_tin_prefix(f'0{i}000')
    for i in range(21, 31):
        assert not tintools.validate_tin_prefix(f'{i}0000')


# -------------------------------------------------------------------------------- #
def test_validate_full_tin_success():
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
        assert tintools.validate_tin_checksum(tin)


# -------------------------------------------------------------------------------- #
def test_validate_full_tin_failure():
    assert not tintools.validate_tin_checksum('4560312650')


# -------------------------------------------------------------------------------- #
def test_validate_full_tin_conversion():
    tin_arr = [int(c) for c in '45603126506']
    assert tintools.validate_tin_checksum(tin_arr)


# -------------------------------------------------------------------------------- #
def test_assemble_full_tin_conversion():
    tin_arr = [int(c) for c in '4560312650']
    assert tintools.assemble_full_tin(tin_arr) == '45603126506'


# -------------------------------------------------------------------------------- #
def test_assemble_full_tin_success():
    tin = tintools.assemble_full_tin('4560312650')
    assert tintools.validate_tin_checksum(tin)


# -------------------------------------------------------------------------------- #
def test_natural_person_tins():
    for _ in range(100):
        tin_date = tintools.generate_tin_date()
        q_num = tintools.generate_tin_queue_num(PersonType.NATURAL)
        full_tin = tintools.assemble_full_tin(tin_date, q_num)
        assert tintools.validate_tin_checksum(full_tin)


# -------------------------------------------------------------------------------- #
def test_get_person_from_tin_failure():
    assert tintools.get_person_from_tin('') is None
    assert tintools.get_person_from_tin('0' * 6) is None
    assert tintools.get_person_from_tin('0' * 9) is None
    assert tintools.get_person_from_tin('0' * 12) is None
    assert tintools.get_person_from_tin('1234567m') is None


# -------------------------------------------------------------------------------- #
def test_get_natural_person_from_tin():
    assert tintools.get_person_from_tin('0' * 10) == PersonType.NATURAL
    assert tintools.get_person_from_tin('0' * 11) == PersonType.NATURAL


# -------------------------------------------------------------------------------- #
def test_get_judicial_person_from_tin():
    assert tintools.get_person_from_tin('0' * 7) == PersonType.JUDICIAL
    assert tintools.get_person_from_tin('0' * 8) == PersonType.JUDICIAL
