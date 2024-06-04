'''
Shitai Stanley Zhao CS5001 Final Project enlarge artwork page
This page lets the user enlarge an artwork of their choosing
But first they need to enter password (Vancouver)
if the password is incorrect, the page won't proceed

classes:
SearchbyID
RandomAndTotal (used for verifyting valid artwork ID)

streamlit module used for password verification:
hmac

Password Validation Reference site: Streamlit official document
https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso
'''

import streamlit as st
import hmac
from models.search_by_id import SearchbyID

st.header("Enlarge an artwork in a new tab")
st.markdown("Where you can right click to save the image")

# This part below is a simple password check function with no user data needed
# Codes from the streamlit official document, with of course my modifications


st.markdown("But first, enter the password to use this function")


def check_password():
    '''Returns True if the user had the correct password.
    Codes are from the streamlit official library
    '''

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"],
                               st.secrets["password"]):
            st.session_state["password_correct"] = True
            # Don't store the password
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the passward is validated
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("Password incorrect")
    return False


if not check_password():
    # This if-else block acts as a check on password validation
    # Do not continue if check_password is not True
    st.stop()

# The password validation part above is over

else:
    # Proceed to the enlarge image feature
    user_input = st.text_input('Password correct. Enter an object ID:')
    if st.button("Find Object"):
        try:
            id_search = SearchbyID(user_input)

            # Input validation
            if not id_search.validate_user_input_non_integer():
                raise TypeError
            elif not id_search.validate_user_input_invalid():
                raise ValueError

            # Proceed if input is valid
            if id_search.fetch_artwork():
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
                if id_search.image is not None:
                    # Construct a hyperlink variable of the large image
                    download_link = f'<a href="{id_search.image}" download>Open Large Image in a New Tab</a>'
                    # use st.markdown to display this link
                    st.markdown(download_link, unsafe_allow_html=True)
                else:
                    st.markdown("There is no available image for this artwork")
            else:
                st.write(f"An error occured for this artwork: {id_search.error}")

        except TypeError:
            st.write("Please enter an integer")
        except ValueError:
            st.write("This ID is invalid. Please enter a valid artwork ID.")
