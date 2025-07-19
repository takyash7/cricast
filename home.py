import streamlit as st
import account

def app():
    st.markdown("<h1 style='color:#DC143C;'>🌟 Welcome to CriCast</h1>", unsafe_allow_html=True)
    st.markdown("##### 🏏 Your Cricket Prediction Companion ")
    st.markdown("##### 🎯 Live Action. Smart Predictions. Real-Time Insights.")
    st.markdown("<h3 style='color:#90EE90;'>🚀 Please sign up or login to continue</h3>", unsafe_allow_html=True)

    option = st.selectbox("Select an option:", ["Chooese","Sign Up", "Login"])
   
    if option == "Login" or option == "Sign Up":
        account.app()
