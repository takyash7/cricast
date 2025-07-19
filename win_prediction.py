import streamlit as st
import pickle
import pandas as pd

def app():

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

    # Load the trained model
    pipe = pickle.load(open('LR_80.pkl', 'rb'))
    
    st.markdown("<h1 style='color:#DC143C;'>📊 Win Predictor</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox('Select the batting team', sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select the bowling team', sorted(teams))

    selected_city = st.selectbox('Select host city', sorted(cities))
    target = st.number_input('Target', min_value=1)
    
    col3, col4, col5 = st.columns(3)
    with col3:
        score = st.number_input('Score', min_value=0)
    with col4:
        overs = st.number_input('Overs completed', min_value=0.1, max_value=20.0, step=0.1)
    with col5:
        wickets = st.number_input('Wickets out', min_value=0, max_value=10)

    if st.button('Predict Probability'):
        if overs == 0:
            st.error("Overs cannot be zero.")
            return
        
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        crr = score / overs
        rrr = (runs_left * 6) / balls_left if balls_left != 0 else 0

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'target': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]

        st.header(f"{batting_team} - {round(win * 100)}% 🏏")
        st.header(f"{bowling_team} - {round(loss * 100)}% 🛡️")
