from rik_app.tools import tintools, gentools, nametools
from rik_app.rik_types import PersonType
from datetime import datetime, date
import pytest


# -------------------------------------------------------------------------------- #
def test_generate_equity():
    for _ in range(100):
        data = gentools.generate_equity()
        assert "equity" in data.keys()
        assert "shares" in data.keys()
        assert isinstance(data.shares, list)
        assert data.equity == sum(data.shares)


# -------------------------------------------------------------------------------- #
def test_generate_iso_date():
    for _ in range(100):
        now = datetime.now().date()
        d = gentools.generate_iso_date()
        assert date.fromisoformat(d) <= now


# -------------------------------------------------------------------------------- #
def test_generate_tin():
    for _ in range(50):
        tin = gentools.generate_tin(PersonType.NATURAL)
        assert tintools.validate_tin_checksum(tin)
    for _ in range(50):
        tin = gentools.generate_tin(PersonType.JUDICIAL)
        assert tintools.validate_tin_checksum(tin)
    with pytest.raises(TypeError):
        gentools.generate_tin("asdfg")


# -------------------------------------------------------------------------------- #
def test_generate_judicial_name():
    for _ in range(100):
        name = gentools.generate_judicial_name()
        assert 'OÜ' in name


# -------------------------------------------------------------------------------- #
def test_generate_shareholder():
    sh = gentools.generate_shareholder(12345, founder=True)
    assert sh.equity == 12345


# -------------------------------------------------------------------------------- #
def test_generate_company_names():
    names = gentools.generate_company_names(100)
    assert len(names) == len(set(names))


# -------------------------------------------------------------------------------- #
def test_generate_company_tins():
    tins = gentools.generate_company_tins(100)
    assert len(tins) == len(set(tins))


# -------------------------------------------------------------------------------- #
def test_generate_company():
    tin = gentools.generate_tin(PersonType.JUDICIAL)
    company = gentools.generate_company(name="Tele2 AS", tin=tin)
    assert nametools.is_valid_name(company.name, PersonType.JUDICIAL)
    assert tintools.get_person_from_tin(company.tin) == PersonType.JUDICIAL
    assert tintools.validate_tin_checksum(company.tin)
    assert company.founding_date <= datetime.now().date()
    summed_equity = sum([sh.equity for sh in company.shareholders])
    assert summed_equity == company.equity


# -------------------------------------------------------------------------------- #
def test_generate_companies():
    companies = gentools.generate_companies(100)
    assert len(companies) == 100
