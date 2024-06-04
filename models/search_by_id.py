'''
Shitai Stanley Zhao CS5001 FInal Project seach_by_id.py
This module has all the methods and attributes of class SearchbyID
Which is a class that mainly deals with the task of user input validation,
and searching an object based on its ID

Module:
requests
RandomAndTotal (used for validating user input)
'''


import requests
from models.random_and_total_artwork import RandomAndTotal


class SearchbyID:
    '''
    SearchbyID is a function-focued class that takes in an id,
    checks if this id is integer or valid if needed, and search for
    this artwork by its ID usign HTTPS requests, stores the original json data,
    and parses through this original data to obtain relevant properties.
    __str__ is redundant in this class.
    '''

    def __init__(self, id):
        self.image = None
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def validate_user_input_non_integer(self):
        '''
        When the self.id comes from user input, validate that it's an integer
        '''
        try:
            self.id = int(self.id)
            return True
        except ValueError:
            return False

    def validate_user_input_invalid(self):
        '''
        When self.id comes from user input and is integer,
        validate this input against the list of valid IDs

        module used: RandomAndTotal
        '''
        if self.id <= 0:
            return False
        else:
            total = RandomAndTotal()
            total.fetch_total_collection()
            return self.id in total.available_artwork_ids

    def fetch_artwork(self):
        '''
        Fetches artwork from the Met API according to the id provided
        and store the data as json file. Returns True if successful,
        False otherwise, and handles client side and server side errors
        '''
        self.api = "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(self.id)
        response = requests.get(self.api)
        if response.status_code == 200:
            self.data = response.json()
            return True
        else:
            self.error = response.status_code
            return False

    def parse_data(self):
        '''
        Parse through the data retrieved,
        and pass the properties to the object itself
        '''
        self.title = self.data["title"]
        self.artist = self.data["artistDisplayName"]
        self.artist_bio = self.data["artistDisplayBio"]
        self.department = self.data["department"]
        self.availability = self.data["isPublicDomain"]
        self.url = self.data["objectURL"]
        if self.availability:
            self.image = self.data["primaryImage"]
