from rik_app.utils import pathutils
from pathlib import Path
import pytest
import os


# -------------------------------------------------------------------------------- #
def test_file_finder_success():
    assert pathutils.file_finder(__file__, "pyproject.toml")


# -------------------------------------------------------------------------------- #
def test_file_finder_failure():
    with pytest.raises(RuntimeError):
        pathutils.file_finder(__file__, "__.__")


# -------------------------------------------------------------------------------- #
def test_find_graphql_schema_file():
    cd = Path(__file__).with_name("schema.graphql")
    cd.touch()
    assert pathutils.find_graphql_schema_file(__file__)
    os.remove(cd)


# -------------------------------------------------------------------------------- #
def test_find_app_config_file():
    cd = Path(__file__).with_name("app.config.toml")
    cd.touch()
    assert pathutils.find_app_config_file(__file__)
    os.remove(cd)
