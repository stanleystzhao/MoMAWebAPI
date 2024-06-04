'''
CS5001 Shitai Zhao test_search_by_id.py
Using pytest module to test search_by_id.py

class: SearchbyID
module: patch, pytest
'''

from models.search_by_id import SearchbyID
from unittest.mock import patch
import pytest


@pytest.fixture
def id_search():
    return SearchbyID(12345)


def test_init(id_search):
    assert id_search.image is None
    assert id_search.id == 12345


def test_eq_pass(id_search):
    id_search_second = SearchbyID(12345)
    assert id_search == id_search_second


def test_eq_fail(id_search):
    id_search_second = SearchbyID(123)
    assert not id_search == id_search_second


def test_validate_user_input_non_integer_pass(id_search):
    # test a normal case where id is an integer
    assert id_search.validate_user_input_non_integer()


def test_validate_user_input_invalid_pass(id_search):
    # test a normal case where id is also valid
    assert id_search.validate_user_input_invalid()


def test_validate_user_input_non_integer_fail():
    # test an abnormal case where id is non-integer
    non_integer_id = SearchbyID("a non-integer")
    assert not non_integer_id.validate_user_input_non_integer()


def test_validate_user_input_invalid_fail_non_positive():
    # test an abnormal case where the integer is non-positive
    invalid_id_search = SearchbyID(0)
    assert not invalid_id_search.validate_user_input_invalid()
    invalid_id_search = SearchbyID(-30)
    assert not invalid_id_search.validate_user_input_invalid()


def test_validate_user_input_invalid_fail_positive_not_valid():
    # test an abnormal case where the positive integer is invalid
    invalid_id_search = SearchbyID(60)
    assert not invalid_id_search.validate_user_input_invalid()


def test_fetch_artwork_pass(id_search):
    with patch('models.search_by_id.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "title": 1,
            "artistDisplayName": 2,
            "artistDisplayBio": 3,
            "department": 4,
            "isPublicDomain": True,
            "objectURL": 5,
            "primaryImage": 6
            }
        assert id_search.fetch_artwork()
        assert id_search.data == {
            "title": 1,
            "artistDisplayName": 2,
            "artistDisplayBio": 3,
            "department": 4,
            "isPublicDomain": True,
            "objectURL": 5,
            "primaryImage": 6
        }


def test_fetch_artwork_fail(id_search):
    with patch('models.search_by_id.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 505
        mock_response.json.return_value = {
            "title": 1,
            "artistDisplayName": 2,
            "artistDisplayBio": 3,
            "department": 4,
            "isPublicDomain": True,
            "objectURL": 5,
            "primaryImage": 6
            }
        assert id_search.fetch_artwork() is False
        assert id_search.error == 505


def test_parse_data(id_search):
    id_search.data = {
            "title": 1,
            "artistDisplayName": 2,
            "artistDisplayBio": 3,
            "department": 4,
            "isPublicDomain": True,
            "objectURL": 5,
            "primaryImage": 6
        }
    id_search.parse_data()
    assert id_search.title == 1
    assert id_search.artist == 2
    assert id_search.artist_bio == 3
    assert id_search.department == 4
    assert id_search.url == 5
    assert id_search.availability is True
    assert id_search.image == 6
