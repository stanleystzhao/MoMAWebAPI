'''
Shitai Stanley Zhao CS5001 FInal Project random_and_total_artwork.py
This module has all the methods and attributes of class RandomAndTotal
that deals with the random object functions and total collections function

Module:
requests
random
'''

import requests
import random

ALL_ARTS_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"


class RandomAndTotal:
    '''
    A class that deals with the randomness and totality of collections of
    this API. It can fetch the total collections of artworks, fetch a random
    artwork according to the available list of artworks, parse through the
    data of this artwork and pass the relevant properties to the object itself
    __str__ and __eq__ would not make sense in this function class,
    so we won't define these methods
    '''

    def __init__(self):
        self.image = None

    def fetch_total_collection(self):
        '''
        Fetches the number of available artworks from the Met API, and
        the list of available IDs, and returns True
        '''

        response = requests.get(ALL_ARTS_URL)
        if response.status_code == 200:
            data = response.json()
            self.total_artwork_number = data["total"]
            self.available_artwork_ids = data["objectIDs"]
            return True
        else:
            self.error = response.status_code
            return False

    def fetch_random_artwork(self):
        '''
        Fetches a random artwork from the Met API according to the list of
        available ids and store the data as json file
        '''
        random_id = random.choice(self.available_artwork_ids)
        self.id = random_id
        self.api = "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(random_id)
        response = requests.get(self.api)
        if response.status_code == 200:
            self.data = response.json()
            return True
        else:
            self.error = response.status_code
            return False

    def parse_data(self):
        '''
        Parse through the data retrieved, and pass
        the artwork properties to the object itself
        '''
        self.title = self.data["title"]
        self.artist = self.data["artistDisplayName"]
        self.artist_bio = self.data["artistDisplayBio"]
        self.department = self.data["department"]
        self.availability = self.data["isPublicDomain"]
        self.url = self.data["objectURL"]
        if self.availability:
            self.image = self.data["primaryImage"]
