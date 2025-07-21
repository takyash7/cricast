import streamlit as st
import pickle
import pandas as pd
import numpy as np
from xgboost import XGBRegressor



def app():

    pipe = pickle.load(open('pipe.pkl', 'rb'))
    
    teams = [
        'Royal Challengers Bengaluru', 'Mumbai Indians', 'Chennai Super Kings',
        'Kolkata Knight Riders', 'Lucknow Super Giants', 'Sunrisers Hyderabad',
        'Rajasthan Royals', 'Gujarat Titans', 'Delhi Capitals', 'Punjab Kings'
    ]
    
    cities = [
        'Bangalore', 'Mumbai', 'Chandigarh', 'Jaipur', 'Bengaluru',
        'Ahmedabad', 'Delhi', 'Durban', 'Unknown', 'Chennai', 'Abu Dhabi',
        'Dubai', 'Kolkata', 'Pune', 'Mohali', 'Cuttack', 'Hyderabad',
        'Sharjah', 'Bloemfontein', 'Cape Town', 'Indore', 'Visakhapatnam',
        'Centurion', 'Lucknow', 'Ranchi', 'Guwahati', 'Dharamsala',
        'New Chandigarh', 'Port Elizabeth', 'Johannesburg', 'Navi Mumbai',
        'Raipur', 'Kimberley', 'East London'
    ]
    
    st.markdown("<h1 style='color:#DC143C;'>🧠 Score Prediction</h1>", unsafe_allow_html=True)
      
    col1, col2 = st.columns(2)
    
    with col1:
        batting_team = st.selectbox('Select batting team', sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select bowling team', sorted(teams))
    
    city = st.selectbox('Select city', sorted(cities))
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        current_score = st.number_input('Current Score')
    with col4:
        overs = st.number_input('Overs done (works for over > 5)')
    with col5:
        wickets = st.number_input('Wickets out')
    
    last_five = st.number_input('Runs scored in last 5 overs')
    
    if st.button('Predict Score'):
        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        crr = current_score / overs
    
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],
            'current_score': [current_score],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'crr': [crr],
            'last_five': [last_five]
        })
    
        result = pipe.predict(input_df)
        #st.text(result)
        st.header("Predicted Score - " + str(int(result[0])))



