'''
Shitai Stanley Zhao CS5001 Final Project department list page
This page lets the user view all artwork departments and their ID.

classes:
Departments
'''

import streamlit as st
from models.departments import Departments

departments = Departments()

st.header("Artwork department List")

if departments.fetch_dictionary():
    st.markdown(f'''There are {len(departments.dictionary)} artwork
                departments in this collection. These department IDs are
                discontinuous (missing IDs 2 and 20), so you will see
                the final ID up to 21.''')

    # for any department, display its ID (key) and name (value)
    for key in departments.dictionary:
        st.write(f"ID {key} | {departments.dictionary[key]}")

else:
    # print error code
    st.write(f"An error occured: {departments.error}")
