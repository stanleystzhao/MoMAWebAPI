'''
Shitai Stanley Zhao CS5001 Final Project artwork list page
This page lets the user view a chosen number fo random artworks
or list all available artworks

classes:
RandomAndTotal
SearchbyID
'''

from models.random_and_total_artwork import RandomAndTotal
from models.search_by_id import SearchbyID
import streamlit as st
import random


def display_total_artworks():
    '''
    This function is invoked when the user chooses to view all artworks
    There are hundreds of thousands of artwork entries, so testing
    is not feasible

    class:
        RandomAndTotal
        SearchbyID
    '''

    # initiates RandomAndTotal object
    total_artwork = RandomAndTotal()
    total_artwork.fetch_total_collection()
    # for every one of the hundreds of thousands of entries,
    # use their ID to display results via SearchbyID class
    for id_entry in total_artwork.available_artwork_ids:
        each_entry = SearchbyID(id_entry)
        if each_entry.fetch_artwork():
            each_entry.parse_data()
            st.write(f"{each_entry.title}, Object ID: {id_entry}")
        else:
            st.write(f"An error occured for this artwork: {each_entry.error}")


# Page title
st.header("Available artworks")
st.markdown('''This page demonstrates a random number of artworks.
                        If an artwork is on Public Domain,
                        there will be an image beneath the title.''')

display_numbers = st.text_input('''Enter how many random artworks
                                    do you want to see:''')


if st.button("See this many random artworks"):

    # Try block where user inputs integer
    try:
        # If statement deals with non-positive integer
        if int(display_numbers) <= 0:
            st.write("Please enter a positive integer")

        else:
            total = RandomAndTotal()
            total.fetch_total_collection()
            i = 1
            # For each artwork, display its title, id, and if possible, image
            for i in range(int(display_numbers)):
                each_entry = SearchbyID(random.choice(total.available_artwork_ids))
                if each_entry.fetch_artwork():
                    each_entry.parse_data()
                    st.write(f"{each_entry.title.strip()}, ID: {each_entry.id}")

                    # Only display image if it's on public domain
                    if each_entry.availability:
                        st.image(f"{each_entry.image}")
                    else:
                        st.write("Not on Public Domain")
                else:
                    st.write(f"An error occured for artwork {each_entry.id}: {each_entry.error}")
                i += 1

    # Exception block deals with non-integer input
    except ValueError:
        st.write("Please input an integer as the number of artworks to see")


if st.button('''See all artwork titles and IDs
             (Warning: hundreds of thousands of entries)'''):
    # invoke the function defined at the beginning of this module
    st.write('''These artworks are discontiunous,
    so you will see some gaps in IDs''')
    display_total_artworks()
