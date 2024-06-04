'''
Shitai Stanley Zhao CS5001 FInal Project seach_by_text.py
This module has all the methods and attributes of class SearchbyText
Which is a class that mainly deals with the task of user input validation,
and searching an object based on the text input

Module:
requests
RandomAndTotal (used for validating user input)
'''


import requests


class SearchbyText:
    '''
    SearchbyText is a function-focued class that takes in a text,
    searches for a list of relevant artworks by using HTTPS requests,
    stores the original json data,
    and parses through this original data to obtain relevant properties
    __str__ and __eq__ doesn't make sense in this class,
    so we don't define these two methods
    '''
    def __init__(self, text):
        self.text = text

    def __eq__(self, other):
        return self.text == other.text

    def fetch_artworks(self):
        '''
        Fetches a dictionary that contains a list of artwork IDs
        that fit the description and store the data as json file
        And handles relevant slient side and server side errors
        '''

        self.api = "https://collectionapi.metmuseum.org/public/collection/v1/search?q=" + str(self.text)
        response = requests.get(self.api)
        if response.status_code == 200:
            self.data = response.json()
            return True
        else:
            self.error = response.status_code
            return False

    def parse_data(self):
        '''
        Parse through the data retrieved, and pass the
        total number of relevant objects and their IDs
        in this endpoint json data to the object itself.
        '''

        self.artwork_numbers = self.data["total"]
        self.artwork_ids = self.data["objectIDs"]
