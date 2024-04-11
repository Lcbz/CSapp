import requests 
import streamlit as st 
from streamlit_lottie import st_lottie

# emoji cheatsheet from https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Our group project", page_icon=":desert_island:", layout= "wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# LOAD ASSETS
lottie_coding = load_lottieurl("https://lottie.host/b7b2d317-51bf-44b5-9055-7e7b99e20e0f/VcunB4HF2M.json")


# HEADER SECTION
with st.container():
    st.subheader("Welcome to our group project!")
    st.title("Weather to go :desert_island:")
    st.write("This app will enable you to check whether or not the weather condition of your travel destination allows the specific activity you have chosen :partying_face:")


# FILTERS
with st.container():
    st.write("----")
    left_column,right_column = st.columns((2,1))
    with left_column:
        st.header("Let's check the feasibility of your vacation!")
        st.write("\n")
        st.write("Travel Destination") 
        st.write("Start Date") 
        st.write("End Date")
        st.write("Activity")
        # insert api and app code

    with right_column:
        st_lottie(lottie_coding,height=350, key="palmier")

# RESULTS
st.write("----")
st.header("Results:sparkles:")
with st.container():
    visualization_column,answer_column = st.columns((1,1))
    with visualization_column:
        st.write("insert visualization of result here")
       # insert visualization code

    with answer_column:
        st.subheader("Our recommendation")
        # insert answer code



