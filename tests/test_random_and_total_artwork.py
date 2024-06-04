'''
CS5001 Shitai Zhao test_random_and_total_artwork.py
Using pytest to test class RandomAndTotal

class: RandomAndTotal
module: patch, pytest
'''

from models.random_and_total_artwork import RandomAndTotal
from unittest.mock import patch
import pytest


@pytest.fixture
def random():
    return RandomAndTotal()


def test_random_init(random):
    assert random.image is None


def test_random_fetch_total_collection_pass(random):
    with patch('models.random_and_total_artwork.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "total": 3, "objectIDs": [
                1, 3, 5
            ]
         }

        random.fetch_total_collection()
        assert random.total_artwork_number == 3
        assert random.available_artwork_ids == [1, 3, 5]


def test_random_fetch_total_collection_fail(random):
    with patch('models.random_and_total_artwork.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "total": 3, "objectIDs": [
                1, 3, 5
            ]
         }

        assert random.fetch_total_collection() is False
        assert random.error == 401


def test_random_fetch_random_artwork_pass(random):
    random.available_artwork_ids = [2, 3, 4, 5]
    with patch('models.random_and_total_artwork.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "key1": 1, "key2": 2
         }

        assert random.fetch_random_artwork()
        assert random.data == {
            "key1": 1, "key2": 2
         }


def test_random_fetch_random_artwork_fail(random):
    random.available_artwork_ids = [2, 3, 4, 5]
    with patch('models.random_and_total_artwork.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 300
        mock_response.json.return_value = {
            "key1": 1, "key2": 2
         }

        assert random.fetch_random_artwork() is False
        assert random.error == 300


def test_parse_data(random):
    random.data = {
        "title": 1,
        "artistDisplayName": 2,
        "artistDisplayBio": 3,
        "department": 4,
        "isPublicDomain": True,
        "objectURL": 5,
        "primaryImage": 6
    }
    random.parse_data()
    assert random.title == 1
    assert random.artist == 2
    assert random.artist_bio == 3
    assert random.department == 4
    assert random.url == 5
    assert random.availability is True
    assert random.image == 6
