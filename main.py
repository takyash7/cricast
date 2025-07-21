import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
load_dotenv()

# Import your app modules
import home, win_prediction, about, score_prediction, info, match,score

# Streamlit page config
st.set_page_config(page_title="CriCast")

# Optional: Google Analytics (skip if not needed)
st.markdown(
    f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={os.getenv('analytics_tag')}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{os.getenv('analytics_tag')}');
    </script>
    """,
    unsafe_allow_html=True
)

# Class for MultiApp Structure
class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run():
        with st.sidebar:
            app = option_menu(
                menu_title='CriCast',
                options=[
                    'Home', 
                    'Score Prediction', 
                    'Win Prediction', 
                    'UpComing Matches', 
                    'Live Score',
                    'Account', 
                    'About'
                ],
                icons=[
                    'house-door-fill',          # Home
                    'graph-up-arrow',           # Score Prediction
                    'award-fill',               # Win Prediction
                    'calendar-event-fill',      # Upcoming Matches
                    'tv',
                    'person-circle',            # Account
                    'info-circle-fill'          # About
                ],
                menu_icon='trophy-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {
                        "color": "white", 
                        "font-size": "20px", 
                        "text-align": "left", 
                        "margin": "0px", 
                        "--hover-color": "red"
                    },
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # Route to the selected app page
        if app == "Home":
            home.app()

        elif app == "Score Prediction":
            if st.session_state.get("signedout"):
                score_prediction.app()
            else:
                st.warning("⚠️ Please SignUp first to access Score Prediction.")
                st.stop()

        elif app == "Win Prediction":
            if st.session_state.get("signedout"):
                win_prediction.app()
            else:
                st.warning("⚠️ Please SignUp first to access Win Prediction.")
                st.stop()

            
        elif app == "UpComing Matches":
            if st.session_state.get("signedout"):
                match.app()
            else:
                st.warning("⚠️ Please SignUp first to access UpComing Matches.")
                if st.button("👤 SignUP"):
                    home.app()
                st.stop()    

        elif app == "Live Score":
            if st.session_state.get("signedout"):
               score.app()
            else:
                st.warning("⚠️ Please SignUp first to access your Live Score.")
                st.stop()

        elif app == "Account":
            if st.session_state.get("signedout"):
                info.app()
            else:
                st.warning("⚠️ Please SignUp first to access your account details.")
        #       st.stop()

        elif app == "About":
            about.app()

    run()
