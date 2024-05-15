import requests 
import streamlit as st 
from streamlit_lottie import st_lottie
import openmeteo_requests
import requests_cache
import pandas as pd
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from retry_requests import retry 
import numpy as np
import plotly.express as px


# emoji cheatsheet from https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Our group project", layout= "wide")

# FUNCTION TO IMPORT IMAGES FROM LOTTIEFILES; source:https://www.youtube.com/watch?v=VqgUkExPvLY&t=350s
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# IMPORTED IMAGES by using the lottiefile function; source:https://www.youtube.com/watch?v=VqgUkExPvLY&t=350s
lottie_tree = load_lottieurl("https://lottie.host/b7b2d317-51bf-44b5-9055-7e7b99e20e0f/VcunB4HF2M.json")
lottie_plane = load_lottieurl("https://lottie.host/6757851f-9875-4093-b1c1-5d57c507bbf9/MpDQEy5CNa.json")

# HEADER SECTION
#first section which give a brief description of our project
with st.container(): 
    st.subheader("Welcome to our group project!")
    st.title("Weather to go :desert_island:") #name of the app
    st.write("This app has two functionalities, based on last year's data:")
    st.write("- It provides you with the best travel destinations depending on your desired activity and the weather forecast with your desired dates") #functionality 1
    st.write("- Or it could provide you with the weather forecast for any travel destination :partying_face:") #functionality 2

# 1ST FUNCTIONALITY: TRAVEL INSPIRATION
#new section about explaining how this function works
with st.container():
    st.write("----")
    st.title("Travel Inspirations:face_with_monocle:")
    st.write("This functionality will give you some inspirations about top travel destinations depending on your choice of activity!")

    #new sub section to divide the section in 2 parts to have the animation on the right
    with st.container():
        left_column,right_column = st.columns((0.8,0.2)) # divides the container into two columns, with 80% width assigned to 'left_column' and 20% width assigned to 'right_column'

        # create a selection box for the user to choose from various activities they might be interested in for their travels
        with left_column: 
            activity = st.selectbox("What do you want to do?",
            ("Please Choose","Art affiliation",
            "Camping",
            "Cross country skiing",
            "Cycling",
            "Carnavals",
            "Hiking",
            "Historical sightseeing",
            "Ice skating",
            "ATV (All-terrain Vehicle)",
            "Rock climbing",
            "Safari",
            "Sailing",
            "Music Festivals",
            "Shopping",
            "Skiing",
            "Snowmobiling",
            "Sunbathing",
            "Surfing",
            "Water safari",
            "Windsurfing"))

            #maps the selected activity to an index number
            def get_activity_index(activity):
                if activity == "Art affiliation":
                    return 0
                elif activity == "Camping":
                    return 1
                elif activity == "Cross country skiing":
                    return 2
                elif activity == "Cycling":
                    return 3
                elif activity == "Carnavals":
                    return 4
                elif activity == "Hiking":
                    return 5
                elif activity == "Historical sightseeing":
                    return 6
                elif activity == "Ice skating":
                    return 7
                elif activity == "ATV (All-terrain Vehicle)":
                    return 8
                elif activity == "Rock climbing":
                    return 9
                elif activity == "Safari":
                    return 10
                elif activity == "Sailing":
                    return 11
                elif activity == "Music Festivals":
                    return 12
                elif activity == "Shopping":
                    return 13
                elif activity == "Skiing":
                    return 14
                elif activity == "Snowmobiling":
                    return 15
                elif activity == "Sunbathing":
                    return 16
                elif activity == "Surfing":
                    return 17
                elif activity == "Water safari":
                    return 18
                elif activity == "Windsurfing":
                    return 19
                else:
                    return -1  #if activity is not found

            index_number = get_activity_index(activity) #this will be used later to fetch data from data base

        # IMAGE AIRPLANE
        with right_column:
            st_lottie(lottie_plane,height=100, key="airplane")

    if index_number >= 0: 

    # MAP VISUALIZATION
        map = pd.read_excel("/Users/lina/Desktop/APP/pages/lat_long.xlsx") #create map, which is a dataframe from the excel database
        df = map.iloc[index_number] #this indicates which lines it should read based on the index_number
        split_value_df = df.str.split(',') #since the values are in one cells, i must separate them into 2 deifferent variables, this line indicates that after ',' its a new variable; source: CHATGPT 'this is my string = 38.80097,-9.37826 ; how can I split it into two strings'
        latitude_df = split_value_df.str[0] #first value is the latitude, right now they are strings
        longitude_df = split_value_df.str[1]#second value is the longitude, right now they are strings
        # Convert latitude and longitude to numeric values, the cells containing the activity won't be converted; source: CHATGPT
        latitude_numeric = pd.to_numeric(latitude_df, errors='coerce')
        longitude_numeric = pd.to_numeric(longitude_df, errors='coerce')
        # Create a new DataFrame with latitude and longitude columns CHATGPT
        places = pd.DataFrame({'latitude': latitude_numeric, 'longitude': longitude_numeric})
        # Drop rows with NaN values, so that the activities are excluded (i.e., rows where latitude or longitude couldn't be converted to numeric);source: CHATGPT'how should I code to exclude any string from my new dataframe'
        places = places.dropna()

    # RESULTS
        # source: CHATGPT'how to disclose result without a button on streamlit'
        if 'results_displayed' not in st.session_state: #CHATGPT Check if results have been displayed; 
            st.session_state.results_displayed = False #CHATGPT Initialize display state

        if not st.session_state.results_displayed: #CHATGPT If results have not been displayed
            st.header("Top five destinations") #CHATGPT Display header for top destinations
            st.map(places, size=80000, color='#990000', zoom=1.6) #CHATGPT Display map visualization
            
            #new section for the dates selection 
            with st.container():
                choice_column, image_column = st.columns((0.75,0.25)) # create two columns to have an image on the right
                with choice_column:
                    st.write('You have the possibility to see the weather forecast for your prefered destination:')
                    data = pd.read_excel("/Users/lina/Desktop/APP/pages/cs.xlsx") # get activities data from excel file
                    data = data.iloc[index_number] # get the right destinations based on index_number
                    data = data.drop(data.index[0]) # drop the first line which is not relevant for the user; source: CHATGPT ' how to take away the first line of a data frame based on a excel file'
                    select_destination = st.radio('Select your prefered destination:', data )  # enable the user to select their preferred location out of the top 5
                    
                    #Source: CHATGPT 'how to get the index of my selection and fetch the same index number object in the data frame'
                    mapping_dict = {index: destination for index, destination in enumerate(data)} # Create mapping dictionary CHATGPT 
                    selected_index = next(index for index, value in mapping_dict.items() if value == select_destination) # Get the index of the selected destination CHATGPT
                    selected_index += 1 #this line is necessary because the original index from the df are larger by 1 unit because there is the title line
                    selected_value_from_df = df.iloc[selected_index] # fetch values from df (for latitude and longitude) CHATGPT

                    split_value = selected_value_from_df.split(',') # again we have the same problem as before, the values are one single string and we must split it in two
                    latitude = split_value[0] #same process as before
                    longitude = split_value[1] #same process as before
                
                    start_date = st.date_input("Start Date") #user input for travel dates, which will be used later on in the weather API
                    end_date = st.date_input("End Date")  #user input for travel dates, which will be used later on in the weather API
                    button1_pressed = st.button('Show Weather')  #create a button 

                with image_column:
                    st_lottie(lottie_tree,height=200, key="palmier") # animation tree

        # WEATHER API: https://open-meteo.com/en/docs/historical-weather-api
            #create a function which will match the meteo code from the api to its meaning; source: https://open-meteo.com/en/docs
            def f_decode_meteo(f_valeur):
                if f_valeur == 0:
                    return "Clear Sky"
                elif f_valeur == 1:
                    return "Mainly Clear"
                elif f_valeur == 2:
                    return "Partly Cloudy"
                elif f_valeur == 3:
                    return "Cloudy"
                elif f_valeur == 45:
                    return "Fog"
                elif f_valeur == 48:
                    return "Depositing Rime Fog"
                elif f_valeur == 51:
                    return "Light Drizzle"
                elif f_valeur == 53:
                    return "Moderate Drizzle"
                elif f_valeur == 55:
                    return "Dense Drizzle"
                elif f_valeur == 56:
                    return "Light Freezing Drizzle"
                elif f_valeur == 57:
                    return "Dense Freezing Drizzle"
                elif f_valeur == 61:
                    return "Slight Rain"
                elif f_valeur == 63:
                    return "Moderate Rain"
                elif f_valeur == 65:
                    return "Heavy Rain"
                elif f_valeur == 66: 
                    return "Light Freezing Rain"
                elif f_valeur == 67: 
                    return "Heavy Freezing Rain"
                elif f_valeur == 71: 
                    return "Slight Snow Fall"
                elif f_valeur == 73: 
                    return "Moderate Snow Fall"
                elif f_valeur == 75: 
                    return "Heavy Snow Fall"
                elif f_valeur == 77: 
                    return "Snoww Grain"
                elif f_valeur == 80: 
                    return "Slight Rain Shower"
                elif f_valeur == 81: 
                    return "Moderate Rain Shower"
                elif f_valeur == 82: 
                    return "Violent Rain Shower"
                elif f_valeur == 85: 
                    return "Slight Snow Shower"
                elif f_valeur == 86: 
                    return "Heavy Snow Shower"
                elif f_valeur == 95: 
                    return "Slight or Moderate Thunderstorm"
                elif f_valeur == 96: 
                    return "Thunderstorm with Slight Hail"
                elif f_valeur == 99: 
                    return "Thunderstorm with Heavy Hail"
                else:
                    return "Indéfini"

            #create a function which will call the api; these are mostly given by the API; source: https://open-meteo.com/en/docs/historical-weather-api
            def AppelApiDaily(My_Date,latitude, longitude):
                # Setup the Open-Meteo API client with cache and retry on error
                cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
                retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
                openmeteo = openmeteo_requests.Client(session = retry_session)
                url = "https://archive-api.open-meteo.com/v1/archive"

                # these are all the variables required for the API to run, source: https://open-meteo.com/en/docs/historical-weather-api
                params = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "start_date": My_Date,
                    "end_date": My_Date,
                    "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"]} #these are the results we will get, notably weather code, max and min temperature
                
                responses = openmeteo.weather_api(url, params=params) #source: https://open-meteo.com/en/docs/historical-weather-api
                response = responses[0] 

                # Process daily data. The order of variables needs to be the same as requested. source: https://open-meteo.com/en/docs/historical-weather-api
                daily = response.Daily()
                daily_weather_code = daily.Variables(0).ValuesAsNumpy()
                daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
                daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()

                Code_Meteo = f_decode_meteo(daily_weather_code)
                Temp_max = daily_temperature_2m_max
                Temp_min = daily_temperature_2m_min
                fRetour = [My_Date, Code_Meteo, Temp_max, Temp_min]
                return fRetour

            # Extract year, month, and day from the user inputs start_date and end_date objects
            start_year, start_month, start_day = start_date.year, start_date.month, start_date.day
            end_year, end_month, end_day = end_date.year, end_date.month, end_date.day
            # Create datetime objects using extracted values
            API_start_date = datetime(start_year, start_month, start_day)
            API_end_date = datetime(end_year, end_month, end_day)
            # Subtracting one year from both dates in order to have historcial data from the weather api
            API_start_date -= relativedelta(years=1)
            API_end_date -= relativedelta(years=1)
            # Calculating the days difference to create a loop after
            Date_diff_nb = pd.Timedelta(API_end_date - API_start_date)
            Nb_days = Date_diff_nb.days +1 # add one to not exclude any days, and make sure this is an integer

            #create empty lists to stock the answers
            table_Dates = [""]
            table_weather_code = [""]
            table_max_temp = [""]
            table_min_temp = [""]
            nb_loops = 1 # limit the number of loops to 1

            #This loop iterates over the number of days specified by Nb_days
            for i in range(0 , Nb_days):   
                current_date = API_start_date + timedelta(days=i) #calculates the current date by adding i days to the starting date API_start_date.
                current_date_str = current_date.strftime('%Y-%m-%d') #Converts the current date to a string in the format YYYY-MM-DD
                retour_function = AppelApiDaily(current_date_str,latitude, longitude) #Calls the function AppelApiDaily to returns weather data for the specified date and location
                print(retour_function)
                table_Dates.append(retour_function[0]) #The 0 in the [] of the retour_function allows to append the weather code from the returned data to the table_weather_code list (created above)
                table_weather_code.append(retour_function[1]) #The 1 in the []  of the retour_function allows to append the weather code from the returned data to the table_weather_code list (created above)
                table_max_temp.append(retour_function[2]) #The 2 in the []  of the retour_function allows to append the maximum temperature from the returned data to the table_max_temp list (created above)
                table_min_temp.append(retour_function[3]) #The 3 in the []  of the retour_function allows to append the minimum temperature from the returned data to the table_min_temp list
                nb_loops = nb_loops + 1 #increases the loop counter nb_loops. This allows to keep track of the number of iterations the first loop has completed to determine the range for the second loop, which prints the collected weather data.

                
            for j in range(1 , nb_loops):  #This loop iterates from 1 to nb_loops
                print(table_Dates[j]) 
                print(' Meteo : ' + table_weather_code[j])  #prints the weather code from the table_weather_code list at index j
                print('Maximum Temperature :', table_max_temp[j]) #prints the maximum temperature from the table_max_temp list at index j
                print('Minimum temperature :', table_min_temp[j])#prints the minimum temperature from the table_min_temp list at index j
        #Thus the first loop purpose is to retrieve weather data for each day in the specified range and store it in corresponding list, then the second loop prints out the stored weather data for each day


        #source: CHATGPT 'how to create a table with dates as colomn name and the other parameters as rows'
        # Creating a dictionary to store the data CHATGPT
        data = {
            'Date': table_Dates[1:nb_loops],
            'Meteo': table_weather_code[1:nb_loops],
            'Maximum Temperature': table_max_temp[1:nb_loops],
            'Minimum Temperature': table_min_temp[1:nb_loops]
        }
        # Creating the DataFrame CHATGPT
        result1 = pd.DataFrame(data, index=table_Dates[1:nb_loops], columns=['Meteo', 'Maximum Temperature', 'Minimum Temperature'])
        result = result1.T # Transposing the DataFrame CHATGPT
        result.index = ['Meteo', 'Max. Temperature [C°]', 'Min. Temperature [C°]'] # Renaming the index CHATGPT

        # transform them to array so that it works in the next function, source: CHATGPT fix bug by giving them my function disply_weather_chart
        max_temps = np.array(table_max_temp[1:nb_loops]) 
        min_temps = np.array(table_min_temp[1:nb_loops])

        def display_weather_chart(data):
            data['avg_temp'] = [(int(max_temp) + int(min_temp)) / 2 for max_temp, min_temp in zip(data['Maximum Temperature'], data['Minimum Temperature'])]
            fig = px.area(data, x='Date', y='avg_temp', title="Average Temperature by Day",
                        labels={'avg_temp': 'Average Temperature (°C)', 'Date': 'Date'},
                        line_shape='spline',
                        color_discrete_sequence=['#FFD700'])
            fig.update_traces(line=dict(color='black'), fillcolor='rgba(104, 214, 206, 0.5)')
            st.plotly_chart(fig, use_container_width=True)
            
        if button1_pressed: #create a condition so that the results are only shown after the button is pressed
            st.header("Weather forecast based on last year's data :sparkles:") #title of results
            with st.container(): #new box to keep things tidy
                    st.table(result) # streamlit funtion to print the table of weather
                    display_weather_chart(data)                    





#2ND FUNCTIONALITY: WEATHER CHECK FOR ANY DESTINATION
with st.container():
    st.write("----")
    st.title("Weather Forecast :sparkles:")
    st.write("This functionality allow you to check the weather forecast of your desired destination and enable you to know if your travel plans are realistic :sm ")
    end_location = st.text_input("Travel Destination") #define travel city which will be used by geocode api
    end_country = st.text_input("Destination Country") #necessary for geocode 1a
    travel_start_date = st.date_input("Travel Start Date") #define new variables for dates
    travel_end_date = st.date_input("Travel End Date")#define new variables for dates
    button = st.button("Check")#create new button 

    if button: # run the apis and print results if the button is printed

    # GEOCODE API; source:https://api-ninjas.com/api/geocoding
        city = end_location #connect user input to api variable
        country = end_country #connect user input to api variable
        api_url = 'https://api.api-ninjas.com/v1/geocoding?city={}&country={}'.format(city, country) #url to call api
        response = requests.get(api_url + city, headers={'X-Api-Key':'pZ5ZFCDiwMUOUj9ftpBsaxAYd87hgNr4J0CFVCNF'}) #response of the api
        if response.status_code == 200:
            resp = response.json()
            if resp and isinstance(resp, list) and len(resp) > 0:
                longitude_part2 = resp[0].get("longitude")
                latitude_part2 = resp[0].get("latitude")
                if longitude_part2 is not None and latitude_part2 is not None:
                    print("Longitude: ", longitude_part2)
                    print("Latitude: ", latitude_part2)
        else:
            print("Error:", response.text)

    # WEATHER API call, same as before
        # Extract year, month, and day from the user inputs start_date and end_date objects
        start_year, start_month, start_day = travel_start_date.year, travel_start_date.month, travel_start_date.day
        end_year, end_month, end_day = travel_end_date.year, travel_end_date.month, travel_end_date.day
        # Create datetime objects using extracted values
        API_start_date = datetime(start_year, start_month, start_day)
        API_end_date = datetime(end_year, end_month, end_day)
        # Subtracting one year from both dates
        API_start_date -= relativedelta(years=1)
        API_end_date -= relativedelta(years=1)
        # Calculating the days difference to create a loop after
        Date_diff_nb = pd.Timedelta(API_end_date - API_start_date) 
        Nb_days = Date_diff_nb.days +1  # add one to not exclude any days, and make sure this is an integer

        #create lists to stock answers from api
        table_Dates = [""]
        table_weather_code = [""]
        table_max_temp = [""]
        table_min_temp = [""]
        nb_loops = 1 #limit loop to 1

        for i in range(0 , Nb_days):   #This loop iterates over the number of days specified by Nb_days
            current_date = API_start_date + timedelta(days=i) #calculates the current date by adding i days to the starting date API_start_date.
            current_date_str = current_date.strftime('%Y-%m-%d') #Converts the current date to a string in the format YYYY-MM-DD
            retour_function = AppelApiDaily(current_date_str,latitude_part2, longitude_part2) #Calls the function AppelApiDaily to returns weather data for the specified date and location
            print(retour_function)
            table_Dates.append(retour_function[0]) #The 0 in the [] of the retour_function allows to append the weather code from the returned data to the table_weather_code list (created above)
            table_weather_code.append(retour_function[1]) #The 1 in the []  of the retour_function allows to append the weather code from the returned data to the table_weather_code list (created above)
            table_max_temp.append(retour_function[2]) #The 2 in the []  of the retour_function allows to append the maximum temperature from the returned data to the table_max_temp list (created above)
            table_min_temp.append(retour_function[3])#The 3 in the []  of the retour_function allows to append the minimum temperature from the returned data to the table_min_temp list
            nb_loops = nb_loops + 1 #increases the loop counter nb_loops. This allows to keep track of the number of iterations the first loop has completed to determine the range for the second loop, which prints the collected weather data. This allows also to dynamically control the number of loops.
            
        for j in range(1 , nb_loops):  #This loop iterates from 1 to nb_loops
            print(table_Dates[j])
            print(' Meteo : ' + table_weather_code[j]) #prints the weather code from the table_weather_code list at index j
            print('Maximum Temperature :', table_max_temp[j]) #prints the maximum temperature from the table_max_temp list at index j
            print('Minimum temperature :', table_min_temp[j])#prints the minimum temperature from the table_min_temp list at index j
        # the first loop purpose is to retrieve weather data for each day in the specified range and store it in corresponding list, then the second loop prints out the stored weather data for each day

        # Creating a dictionary to store the new results, same process as functionality 1
        weather = {
            'Date': table_Dates[1:nb_loops],
            'Meteo': table_weather_code[1:nb_loops],
            'Maximum Temperature': table_max_temp[1:nb_loops],
            'Minimum Temperature': table_min_temp[1:nb_loops]
        }

        # Creating the DataFrame
        dw = pd.DataFrame(weather, index=table_Dates[1:nb_loops], columns=['Meteo', 'Maximum Temperature', 'Minimum Temperature'])
        dw = dw.T # Transposing the DataFrame
        dw.index = ['Meteo', 'Max. Temperature [C°]', 'Min. Temperature [C°]'] # Renaming the index for the final table to be as i want

    # RESULTS
        st.write("----")
        st.header("Last year's Weather suggests")
        with st.container():
            st.table(dw) #show the table
            display_weather_chart(weather) #show the chart
