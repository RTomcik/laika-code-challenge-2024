import configparser
import os
import sys

import pytest


# Ensure root is present in path
# TODO Add to an init of conftest?
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)

import utils.shotgrid


@pytest.fixture
def mock_valid_config():
    """Mock Config file"""
    config = configparser.ConfigParser()
    config["SHOTGRID_API"] = {
        "SHOTGRID_URL": "TESTURL",
        "SCRIPT_NAME": "TESTSCRIPT",
        "API_KEY": "TESTAPIKEY",
    }
    return config


@pytest.fixture
def mock_missing_section_config():
    """Mock Config file missing the SHOTGRID_API section"""
    config = configparser.ConfigParser()
    return config


@pytest.fixture
def mock_missing_field_config():
    """Mock Config file missing one of the required fields"""
    config = configparser.ConfigParser()
    config["SHOTGRID_API"] = {
        "SCRIPT_NAME": "TESTSCRIPT",
        "API_KEY": "TESTAPIKEY",
    }
    return config


def test_get_shotgrid_python_client(mocker, mock_valid_config): ...


def test_validate_config(mock_valid_config):
    """Tests a valid config against the validation function"""
    response = utils.shotgrid._validate_config(mock_valid_config)
    assert response is None


def test_validate_config_missing_section(mock_missing_section_config):
    """Tests a config missing the SHOTGRID_API section"""
    response = utils.shotgrid._validate_config(mock_missing_section_config)
    assert (
        response == "The 'SHOTGRID_API' section is missing from your "
        "conf.ini file."
    )


def test_validate_config_missing_field(mock_missing_field_config):
    """Tests a config missing a field from the SHOTGRID_API section"""
    response = utils.shotgrid._validate_config(mock_missing_field_config)
    assert (
        response == "One of the required fields under the SHOTGRID_API "
        "section is missing from your conf.ini file."
    )
