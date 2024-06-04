'''
Shitai Stanley Zhao CS5001 FInal Project seach_by_title.py
This module has all the methods and attributes of class SearchbyTitle
Which is a class that mainly deals with the task of user input validation,
and searching an object based on the text input, exclusively on their titles

Module:
requests
'''

import requests


class SearchbyTitle:
    '''
    SearchbyText is a function-focued class that takes in a text,
    searches for a list of relevant artworks that have the text in its titles,
    by using HTTPS requests, stores the original json data,
    and parses through this original data to obtain relevant properties.
    __str__ is redundant in this class
    '''

    def __init__(self, text):
        self.image = None
        self.text = text

    def __eq__(self, other):
        return self.text == other.text

    def fetch_artworks(self):
        '''
        Fetches a dictionary that contains a list of artwork IDs
        that fit the description and store the data as json file
        '''
        self.api = "https://collectionapi.metmuseum.org/public/collection/v1/search?title=true&q=" + str(self.text)
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
        properties to the object itself.
        There are only the total numbers and object IDs
        in this endpoint json file
        '''
        self.artwork_numbers = self.data["total"]
        self.artwork_ids = self.data["objectIDs"]
