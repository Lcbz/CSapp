import requests 
import streamlit as st 
from streamlit_lottie import st_lottie
import googlemaps
import openmeteo_requests
import requests_cache
import pandas as pd
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from retry_requests import retry 
import numpy as np



# emoji cheatsheet from https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Our group project", layout= "wide")

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

        start_location = st.text_input("Start Location")

        end_location = st.text_input("Travel Destination")
        end_country = st.text_input("Destination Country")

        travel_start_date = st.date_input("Travel Start Date") 

        travel_end_date = st.date_input("Travel End Date")

        option = st.selectbox("Activity", 
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

    button_pressed = st.button("Check")
if button_pressed:   
# GEOCODE API
    city = end_location
    country = end_country
    api_url = 'https://api.api-ninjas.com/v1/geocoding?city={}&country={}'.format(city, country)
    response = requests.get(api_url + city, headers={'X-Api-Key':'pZ5ZFCDiwMUOUj9ftpBsaxAYd87hgNr4J0CFVCNF'})

    if response.status_code == 200:
        resp = response.json()
        if resp and isinstance(resp, list) and len(resp) > 0:
            longitude = resp[0].get("longitude")
            latitude = resp[0].get("latitude")
            if longitude is not None and latitude is not None:
                st.write("Longitude: ", longitude)
                st.write("Latitude: ", latitude)
    else:
        print("Error:", response.text)


    # WEATHER API 
    def f_decode_meteo(f_valeur):
        if f_valeur == 0:
            return "Clear Sky"
        elif f_valeur == 1:
            return "Slight Cloudy"
        elif f_valeur == 2:
            return "Cloudy"
        elif f_valeur == 61:
            return "Slight Rain"
        elif f_valeur == 63:
            return "Moderate Rain"
        elif f_valeur == 63:
            return "Moderate Rain"
        else:
            return "Indéfini"

    def AppelApiDaily(MaDate,latitude, longitude):

        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
        
        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": MaDate,
            "end_date": MaDate,
            "daily": ["weather_code", "precipitation_sum"]}
        
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        
        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_weather_code = daily.Variables(0).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(1).ValuesAsNumpy()

        daily_data = [MaDate, daily_weather_code, daily_precipitation_sum ]
        
        daily_dataframe = pd.DataFrame(data = daily_data)
        # print(daily_dataframe)

        MaDateTxt = MaDate
        MonCodeMeteo = f_decode_meteo(daily_weather_code)
        fRetour = [MaDateTxt, MonCodeMeteo]
        return fRetour

    # Extract year, month, and day from the datetime.date objects
    start_year, start_month, start_day = travel_start_date.year, travel_start_date.month, travel_start_date.day
    end_year, end_month, end_day = travel_end_date.year, travel_end_date.month, travel_end_date.day

    # Create datetime objects using extracted values
    API_start_date = datetime(start_year, start_month, start_day)
    API_end_date = datetime(end_year, end_month, end_day)

    # Subtracting one year from both dates
    API_start_date -= relativedelta(years=1)
    API_end_date -= relativedelta(years=1)
    API_start_date_str = API_start_date.strftime('%Y-%m-%d')
    API_end_date_str = API_end_date.strftime('%Y-%m-%d')


    # Calculating the difference (Remove print in production)
    DateDiffNb = pd.Timedelta(API_end_date - API_start_date) # nbre de jours entre les dates
    Nbdays = DateDiffNb.days +1 # convertir les jours du format Timedelta en integer
    tableDates = [""]
    tableCodesMeteo = [""]
    NbLoops = 1
    for i in range(0 , Nbdays):   
        DateDateCourante = API_start_date + timedelta(days=i)
        DateDateCourante_str = DateDateCourante.strftime('%Y-%m-%d')
        retourDelaFonction = AppelApiDaily(DateDateCourante_str,latitude, longitude)
        print(retourDelaFonction)
        tableDates.append(retourDelaFonction[0])
        tableCodesMeteo.append(retourDelaFonction[1]) 
        NbLoops = NbLoops + 1
        
    for j in range(1 , NbLoops):  
        print(tableDates[j] + ' Meteo :   ' + tableCodesMeteo[j])


    #TRANSPORTATION API
    def get_transport_options(start_location, end_location, api_key):
        
        gmaps = googlemaps.Client(key=api_key)

        # Define the transportation modes
        modes = ['driving', 'walking', 'bicycling', 'transit']

        transport_options ={} 
        for mode in modes:
            # Request directions for each transportation mode
            directions_result = gmaps.directions(start_location, end_location, mode=mode)

            # If directions are available for the mode, add it to the dict
            if directions_result:
                duration = directions_result[0]['legs'][0]['duration']['text']
                transport_options[mode] = duration

        return transport_options
    api_key = 'AIzaSyCScbqoNpQMkP2ZK1oOlrGynyDs69Qdm8k'
    print(get_transport_options(start_location, end_location, api_key))

# ANIMATION TREE
with right_column:
        st_lottie(lottie_coding,height=470, key="palmier")

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
        if button_pressed:
            st.write("For your trip from", start_location, "to",end_location, "in order to explore", option,":")
            st.write("Sustainable itinerary options:", get_transport_options(start_location, end_location, api_key))
            for j in range(1 , NbLoops):  
                st.write(tableDates[j] + ' Meteo :   ' + tableCodesMeteo[j])
            
        # insert answer code