"""
Utility wrapper to connect to a specific shotgrid DB using a config file.
"""

from typing import Union

import logging
import configparser
import shotgun_api3


def get_shotgrid_python_client() -> Union[shotgun_api3.Shotgun | None]:
    """
    Wrapper to fetch a shotgun_api3.Shotgun object using credentials and keys
    stored in the projects conf.ini.

    Returns:
        shotgun_api3.Shotgun - A SG object with the config credentials loaded.
        Returns None if there was an issue reading from the config file.
    """
    config = configparser.ConfigParser(interpolation=None)
    config.read("conf.ini")
    validation_error = _validate_config(config)
    if validation_error:
        logging.error(validation_error)
        return None

    sg = shotgun_api3.Shotgun(
        config["SHOTGRID_API"]["SHOTGRID_URL"],
        script_name=config["SHOTGRID_API"]["SCRIPT_NAME"],
        api_key=config["SHOTGRID_API"]["API_KEY"],
    )
    return sg


def _validate_config(config: configparser.ConfigParser) -> str:
    """
    Validates that the necessary config values are present to instantiate a SG
    connection object.

    Args:
        config (ConfigParser): The loaded config object to validate.

    Returns:
        str - An empty string is the validation passes, otherwise an error
        print out if validation fails.
    """
    try:
        shotgrid_api_section = config["SHOTGRID_API"]
    except KeyError:
        return "The 'SHOTGRID_API' section is missing from your conf.ini file."

    try:
        section_keys = shotgrid_api_section.keys()
        assert "SHOTGRID_URL" in section_keys
        assert "SCRIPT_NAME" in section_keys
        assert "API_KEY" in section_keys
    except AssertionError:
        return "One of the required fields under the SHOTGRID_API section is" \
            " missing from your conf.ini file."
