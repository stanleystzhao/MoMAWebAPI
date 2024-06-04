'''
Shitai Stanley Zhao CS5001 FInal Project departments.py
This module has all the methods and attributes of class Department
that deals with the artwork department endpoint

Module:
requests
random
'''

import requests

DEPARTMENT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/departments"


class Departments:
    '''
    A class of deparments that specifically deals with the artwork departments
    that includes that total number of departments, their IDs and their names
    __eq__ and __str__ won't make sense in this class.
    '''

    def __init__(self) -> None:
        self.data = None
        self.dictionary = {}

    def fetch_dictionary(self):
        '''
        fetches the dictionary of available departments and parse
        through the data to pass them to a more orgnaised dictionary
        '''
        response = requests.get(DEPARTMENT_URL)
        if response.status_code == 200:
            self.data = response.json()
            for entry in self.data.get("departments", []):
                self.dictionary[entry["departmentId"]] = entry["displayName"]
            return True
        else:
            self.error = response.status_code
            return False
