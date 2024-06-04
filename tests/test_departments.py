'''
CS5001 Shitai Zhao test_random_and_total_artwork.py
Using pytest to test class Departments

class: Departments
module: patch, pytest
'''

from models.departments import Departments
from unittest.mock import patch
import pytest


@pytest.fixture
def dep():
    return Departments()


def test_departments_init(dep):
    assert dep.data is None
    assert dep.dictionary == {}


def test_departments_fetch_dictionary_pass(dep):
    with patch('models.departments.requests.get') as mock_get:

        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "departments": [
                {
                    "departmentId": 1,
                    "displayName": "American Decorative Arts"
                }
            ]
        }
        assert dep.fetch_dictionary() is True
        assert dep.data == {
            "departments": [
                {"departmentId": 1, "displayName": "American Decorative Arts"}
            ]
        }
        assert dep.dictionary == {1: "American Decorative Arts"}


def test_departments_fetch_dictionary_fail(dep):
    with patch('models.departments.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.json.return_value = {}
        assert dep.fetch_dictionary() is False
        assert dep.error == 404
