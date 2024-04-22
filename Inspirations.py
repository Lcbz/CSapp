import requests 
import streamlit as st 
import pandas as pd
from streamlit_lottie import st_lottie

# emoji cheatsheet from https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Our group project", layout= "wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# IMPORTED IMAGES
lottie_coding = load_lottieurl("https://lottie.host/6757851f-9875-4093-b1c1-5d57c507bbf9/MpDQEy5CNa.json")


# HEADER SECTION
with st.container():
    st.title("Travel Inspirations:face_with_monocle:")
    st.write("This functionality will give you some inspirations about Top travel destinations depending on your choice of activity!")


# FILTERS
with st.container():
    st.write("----")
    left_column,right_column = st.columns((1,1.5))
    with left_column:
        st.header("Activities:sparkles:")
        st.write("\n")

        activities = st.radio("What do you want to do?",
        ("Art affiliation",
        "Camping",
        "Cross country skiing",
        "Cycling",
        "Carnavals",
        "Hiking",
        "Historical sightseeing",
        "Ice skating",
        "Quadding",
        "Rockclimbing",
        "Safari",
        "Sailing",
        "Seven wonders of the world",
        "Shopping",
        "Skiing",
        "Snowmobiling",
        "Sunbathing",
        "Surfing",
        "Water safari",
        "Windsurfing"))

    button_pressed = st.button("Show Top Destinations")

# IMAGE AIRPLANE
    with right_column:
        st_lottie(lottie_coding,height=620, key="airplane")

# RESULTS
st.write("----")
st.header("Top Destinations :sparkles:")
with st.container():
    if button_pressed: st.write ("Here are our recommendations!")
    visualization_column = st.write("insert visualization of result here")
      
       # insert visualization code




