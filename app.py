'''
Shitai Stanley Zhao CS5001 Final Project app page
This is the main welcome page of the application,
where we can see what this website is about,
the total number of available artworks,
and choose to view a random artwork

class:
RandomAndTotal
'''

import streamlit as st
from models.random_and_total_artwork import RandomAndTotal

# title
st.header("The Metropolitan Museum of Art Collections")
st.markdown('''Welcome! This is an artwork-themed application, and it lets
            you explore artworks from the
            Metropolitan Museum of Art.''')

# object initiation: initiate an object that does random search and total fetch
random_artwork = RandomAndTotal()

# fetch the total available number of artworks to display up front
if random_artwork.fetch_total_collection():
    st.markdown(f'''Total number of available artworks:
                {random_artwork.total_artwork_number}''')
else:
    # display an error message
    st.write(f'''A error occured while fetching the total number of
             artworks: {random_artwork.error}''')

# fetch a random artwork
if st.button("View a random artwork"):
    if random_artwork.fetch_random_artwork():
        random_artwork.parse_data()
        # Display the object properties
        st.markdown(f"Title: {random_artwork.title.strip()}")
        st.markdown(f"ID: {random_artwork.id}")

        # Only display author and its brief biography if there is one
        if random_artwork.artist != "" and random_artwork.artist_bio != "":
            st.markdown(f'''Artist: {random_artwork.artist}
                        ({random_artwork.artist_bio})''')
        elif random_artwork.artist != "" and random_artwork.artist_bio == "":
            st.markdown(f"Artist: {random_artwork.artist}")

        st.markdown(f"Artwork Department: {random_artwork.department}")

        # Only display image if it's on Public Domain
        if random_artwork.availability:
            st.image(random_artwork.image)
        else:
            st.markdown("Unfortunately, this artwork is not on public domain")

        st.markdown(f"The artwork's Met page: {random_artwork.url}")
        st.markdown(f"Its API page: {random_artwork.api}")

    else:
        st.write(f'''An error occured while fetching a random
                 artwork: {random_artwork.error}''')
