from rik_app.tools import nametools
from rik_app.rik_types import *


# -------------------------------------------------------------------------------- #
def test_is_valid_name_char_natural():
    assert nametools.is_valid_name(' ', PersonType.NATURAL)
    assert nametools.is_valid_name('ß', PersonType.NATURAL)
    for c in "()'.&/,1234567890":
        assert not nametools.is_valid_name(c, PersonType.NATURAL)
    assert not nametools.is_valid_name("12345678", PersonType.NATURAL)


# -------------------------------------------------------------------------------- #
def test_is_valid_name_char_judicial():
    assert nametools.is_valid_name(' ', PersonType.JUDICIAL)
    assert nametools.is_valid_name('ß', PersonType.JUDICIAL)
    assert nametools.is_valid_name('&', PersonType.JUDICIAL)
    assert not nametools.is_valid_name("12345678", PersonType.JUDICIAL)


# -------------------------------------------------------------------------------- #
def test_name_preprocessing():
    name, words = nametools.preprocess("ABC DEF GHI")
    assert name == "abc def ghi"
    assert words == ["abc", "def", "ghi"]


# -------------------------------------------------------------------------------- #
def test_name_id_count():
    assert nametools.get_identifier_count("ABC") == 0
    assert nametools.get_identifier_count("ABCOÜ") == 0
    assert nametools.get_identifier_count("ABC OÜ") == 1
    assert nametools.get_identifier_count("ABCOsaühing") == 1
    assert nametools.get_identifier_count("ABC Osaühing") == 1
    assert nametools.get_identifier_count("OÜ ABC oü") == 2
    assert nametools.get_identifier_count("Osaühing ABC oü") == 2
    assert nametools.get_identifier_count("Osaühing ABC osaühing") == 2


# -------------------------------------------------------------------------------- #
def test_name_id_value():
    assert nametools.get_identifier_value("Osaühing ABC") == "osaühing"
    assert nametools.get_identifier_value("Aktsiaselts ABC") == "aktsiaselts"
    assert nametools.get_identifier_value("ABC OÜ") == "oü"
    assert nametools.get_identifier_value("ABC AS") == "as"
    assert nametools.get_identifier_value("ABCOsaühing") is None
    assert nametools.get_identifier_value("ABC") is None


# -------------------------------------------------------------------------------- #
def test_name_id_position():
    assert nametools.get_identifier_position("Osaühing ABC") == 0
    assert nametools.get_identifier_position("ABC Osaühing") == -1
    assert nametools.get_identifier_position("OÜ ABC") == 0
    assert nametools.get_identifier_position("ABC OÜ") == -1
    assert nametools.get_identifier_position("ABCOÜ") is None
    assert nametools.get_identifier_position("ABC OÜ DEF") is None
    assert nametools.get_identifier_position("OsaühingABC") is None
    assert nametools.get_identifier_position("ABC Osaühing DEF") is None


# -------------------------------------------------------------------------------- #
def test_is_valid_id_count():
    assert nametools.is_valid_id_count("Osaühing ABC")
    assert nametools.is_valid_id_count("OÜ ABC")
    assert not nametools.is_valid_id_count("OÜ ABC Osaühing")
    assert not nametools.is_valid_id_count("OÜ ABC OÜ")
    assert not nametools.is_valid_id_count("Osaühing ABC Osaühing")


# -------------------------------------------------------------------------------- #
def test_is_valid_id_value():
    assert nametools.is_valid_id_value("ABC Osaühing")
    assert nametools.is_valid_id_value("ABC OÜ")
    assert not nametools.is_valid_id_value("ABCOsaühing")
    assert not nametools.is_valid_id_value("ABCOÜ")


# -------------------------------------------------------------------------------- #
def test_is_valid_id_position():
    assert nametools.is_valid_id_position("ABC Osaühing")
    assert nametools.is_valid_id_position("Osaühing ABC")
    assert nametools.is_valid_id_position("ABC OÜ")
    assert nametools.is_valid_id_position("OÜ ABC")
    assert not nametools.is_valid_id_position("ABC OÜ DEF")
    assert not nametools.is_valid_id_position("ABC Osaühing DEF")


# -------------------------------------------------------------------------------- #
def test_get_person_from_name_failure():
    assert nametools.get_person_from_name('') is None


# -------------------------------------------------------------------------------- #
def test_get_natural_person_from_name():
    assert nametools.get_person_from_name('ABC') == PersonType.NATURAL
    assert nametools.get_person_from_name('ABC DEF') == PersonType.NATURAL
    assert nametools.get_person_from_name('ABCOÜ') == PersonType.NATURAL


# -------------------------------------------------------------------------------- #
def test_get_judicial_person_from_name():
    assert nametools.get_person_from_name('ABC OÜ') == PersonType.JUDICIAL
    assert nametools.get_person_from_name('oü ABC') == PersonType.JUDICIAL
    assert nametools.get_person_from_name('ABC osaühing') == PersonType.JUDICIAL
    assert nametools.get_person_from_name('Osaühing ABC') == PersonType.JUDICIAL
    assert nametools.get_person_from_name('ABCOsaühing') == PersonType.JUDICIAL
