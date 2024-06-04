'''
CS5001 Shitai Zhao test_search_by_title.py
Using pytest module to test SearchbyTitle

class: SearchbyTitle
module: patch, pytest
'''

from models.search_by_title import SearchbyTitle
from unittest.mock import patch
import pytest


@pytest.fixture
def title_search():
    return SearchbyTitle("title")


def test_init(title_search):
    assert title_search.text == "title"


def test_eq_pass(title_search):
    title_search_second = SearchbyTitle("title")
    assert title_search == title_search_second


def test_eq_fail(title_search):
    title_search_second = SearchbyTitle("another title")
    assert not title_search == title_search_second


def test_fetch_artwork_pass(title_search):
    with patch('models.search_by_title.requests.get') as mock_get:
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
        assert title_search.fetch_artworks()
        assert title_search.data == {
            "total": 3,
            "objectIDs": [
                1,
                2,
                3
            ]
        }


def test_fetch_artwork_fail(title_search):
    with patch('models.search_by_title.requests.get') as mock_get:
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
        assert not title_search.fetch_artworks()
        assert title_search.error == 404


def test_parse_data(title_search):
    title_search.data = {
        "total": 3,
        "objectIDs": [
            1,
            2,
            3
        ]
    }
    title_search.parse_data()
    assert title_search.artwork_numbers == 3
    assert title_search.artwork_ids == [1, 2, 3]
