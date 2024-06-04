'''
CS5001 Shitai Zhao test_search_by_text.py
Using pytest module to test SearchbyText

class: SearchbyText
module: patch, pytest
'''

from models.search_by_text import SearchbyText
from unittest.mock import patch
import pytest


@pytest.fixture
def text_search():
    return SearchbyText("12345")


def test_init(text_search):
    assert text_search.text == "12345"


def test_eq_pass(text_search):
    text_search_second = SearchbyText("12345")
    assert text_search == text_search_second


def test_eq_fail(text_search):
    text_search_second = SearchbyText("another string")
    assert not text_search == text_search_second


def test_fetch_artwork_pass(text_search):
    with patch('models.search_by_text.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "total": 3,
            "objectIDs": [
                1,
                2,
                3
            ]
        }
        assert text_search.fetch_artworks()
        assert text_search.data == {
            "total": 3,
            "objectIDs": [
                1,
                2,
                3
            ]
        }


def test_fetch_artwork_fail(text_search):
    with patch('models.search_by_text.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "total": 3,
            "objectIDs": [
                1,
                2,
                3
            ]
        }
        assert not text_search.fetch_artworks()
        assert text_search.error == 404


def test_parse_data(text_search):
    text_search.data = {
        "total": 3,
        "objectIDs": [
            1,
            2,
            3
        ]
    }
    text_search.parse_data()
    assert text_search.artwork_numbers == 3
    assert text_search.artwork_ids == [1, 2, 3]
