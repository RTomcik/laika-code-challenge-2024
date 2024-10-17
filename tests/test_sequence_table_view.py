import configparser
import os
import sys

import pytest


# Ensure root is present in path
# TODO Add to an init of conftest?
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)

import sequence_table_view


@pytest.fixture
def mock_sg(mocker):
    """Mock shotgun_api3.Shotgun object"""
    return mocker.Mock()


@pytest.fixture
def mock_sg_project(mocker):
    """Mock for an SG Project entity dictionary"""
    return {"id": 5, "name": "Cool Test Project", "type": "Project"}


@pytest.fixture
def mock_sequences(mocker):
    """Mock for a list of SG sequence entity dictionaries"""
    return [
        {"id": 300, "type": "Sequence"},
        {"id": 301, "type": "Sequence"},
    ]


def test_open_sequence_table(mocker, mock_sg, mock_sg_project, mock_sequences):
    mock_sg.find_one.return_value = mock_sg_project
    mock_sg.find.return_value = mock_sequences
    mock_func_shotgrid_client = mocker.patch(
        "utils.shotgrid.get_shotgrid_python_client", return_value=mock_sg
    )
    mock_func_build_table_data = mocker.patch(
        "sequence_table_view._build_table_data"
    )
    mock_func_build_html = mocker.patch("sequence_table_view._build_html")
    mock_func_write_and_open_html_file = mocker.patch(
        "sequence_table_view._write_and_open_html_file"
    )

    response = sequence_table_view.open_sequence_table(10)
    assert response is None
    mock_sg.find_one.assert_called_once()
    mock_sg.find.assert_called_once()
    mock_func_shotgrid_client.assert_called_once()
    mock_func_build_table_data.assert_called_once()
    mock_func_build_html.assert_called_once()
    mock_func_write_and_open_html_file.assert_called_once()


def test_write_and_open_html_file(): ...


def test_build_table_data(): ...


def test_evaluate_shotgrid_query_field(): ...


def test_parse_filters_from_conditions(): ...


def test_build_html(): ...


def test_get_html_template(): ...
