'''
Shitai Stanley Zhao CS5001 Final Project searches page
This page lets the user search for artworks by ID,
simple text or by title only

classes:
SearchbyID, SearchbyText, SearchbyTitle
'''


import streamlit as st
from models.search_by_text import SearchbyText
from models.search_by_title import SearchbyTitle
from models.search_by_id import SearchbyID

st.header("Searches: by ID, by text, and title")
st.markdown("Search an artwork by what you enter below. "
            "It will return a list of artworks that satisfies your search. ")
st.markdown("Search by ID allows you to find an artwork by its unique ID;")
st.markdown('''Search by text allows you to find a list of artworks that have
            your input in its data, whether it's in its title, artist, artist
            biography, descriptions or any other attribute of this artwork;''')
st.markdown('''Search by title only looks for artworks that have your input
            in its titles (it doesn't look into other attributes).''')

user_input = st.text_input('Enter what you want to search:')

if st.button("Search by ID"):
    try:
        id_search = SearchbyID(user_input)

        # Input validation
        if not id_search.validate_user_input_non_integer():
            raise TypeError
        elif not id_search.validate_user_input_invalid():
            raise ValueError
        elif id_search.fetch_artwork():
            # Valid artwork ID
            id_search.parse_data()
            st.subheader('Search Result:')
            st.markdown(f"Title: {id_search.title.strip()}")
            # Only display author and its brief biography if there is one
            if id_search.artist != "" and id_search.artist_bio != "":
                st.markdown(f"Artist: {id_search.artist} ({id_search.artist_bio})")
            elif id_search.artist != "" and id_search.artist_bio == "":
                st.markdown(f"Artist: {id_search.artist}")
            st.markdown(f"Artwork Department: {id_search.department}")
            # Only display image if it's on Public Domain
            if id_search.availability:
                st.image(id_search.image)
            else:
                st.markdown("Unfortunately, this artwork is not on public domain")

            st.markdown(f"The artwork's Met page: {id_search.url}")
            st.markdown(f"Its API page: {id_search.api}")
        else:
            st.write(f"An error occured for this artwork: {id_search.error}")

    except TypeError:
        st.write("Please enter an integer")
    except ValueError:
        st.write("This ID is invalid. Please enter a valid artwork ID.")


if st.button("Search by simple text"):
    text_search = SearchbyText(user_input)
    if text_search.fetch_artworks():
        text_search.parse_data()

    st.subheader('Search Results:')
    st.markdown(f'''Total number of artwork that have your text in its data
                (including title, artist, department, and so on):
                {text_search.artwork_numbers}''')

    # don't continue if there's no relevant artworks
    if text_search.artwork_numbers != 0:
        # for every entry, use SearchbyID to display its title and ID
        for text_entry_id in text_search.artwork_ids:
            artwork_entry = SearchbyID(text_entry_id)
            if artwork_entry.fetch_artwork():
                artwork_entry.parse_data()
                st.write(f"{artwork_entry.title.strip()}, ID: {artwork_entry.id}")
            else:
                st.write(f"An error occured for this artwork: {artwork_entry.error}")

if st.button("Search by title only"):
    title_search = SearchbyTitle(user_input)
    if title_search.fetch_artworks():
        title_search.parse_data()
    st.subheader('Search Results:')
    st.markdown(f'''Total number of artwork that have your text in its title
                (title only): {title_search.artwork_numbers}''')

    if title_search.artwork_numbers != 0:
        # for every entry, use SearchbyID to display its title and ID
        for title_entry_id in title_search.artwork_ids:
            artwork_entry = SearchbyID(title_entry_id)
            if artwork_entry.fetch_artwork():
                artwork_entry.parse_data()
                st.write(f"{artwork_entry.title.strip()}, ID: {artwork_entry.id}")
            else:
                st.write(f"An error occured for this artwork: {artwork_entry.error}")
