import streamlit as st
import firebase_admin
from firebase_admin import credentials
import json
import requests
import re

# Initialize Firebase
cred = credentials.Certificate("your file")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

def app():
    st.markdown("<h2 style='color:	#DC143C;'> CriCast 🏏</h2>", unsafe_allow_html=True)
   
    # Session state initialization
    for key in ["username", "useremail", "signedout", "signout"]:
        if key not in st.session_state:
            st.session_state[key] = '' if key in ["username", "useremail"] else False

    # Email format check
    def is_valid_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    # Password strength check
    def is_strong_password(password):
        return (
            len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        )

    # Firebase Signup
    def sign_up_with_email_and_password(email, password, username=None):
        try:
            url = "your url"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            if username:
                payload["displayName"] = username
            res = requests.post(url, params={"key": "AIzaSyBipj5KGuXkaDkViRaeBIbAewJ4XYSJFZA"}, data=json.dumps(payload))
            return res.json().get('email', res.json())
        except Exception as e:
            st.error(f'🚫 Signup failed: {e}')

    # Firebase Signin
    def sign_in_with_email_and_password(email, password):
        try:
            url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            res = requests.post(url, params={"key": "AIzaSyBipj5KGuXkaDkViRaeBIbAewJ4XYSJFZA"}, data=json.dumps(payload))
            data = res.json()
            return {
                'email': data['email'],
                'username': data.get('displayName', '')
            }
        except Exception as e:
            st.error(f'🚫 Signin failed: {e}')

    # Reset Password
    def reset_password(email):
        try:
            url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            res = requests.post(url, params={"key": "AIzaSyBipj5KGuXkaDkViRaeBIbAewJ4XYSJFZA"}, data=json.dumps(payload))
            if res.status_code == 200:
                return True, "Reset email sent"
            else:
                return False, res.json().get('error', {}).get('message', 'Unknown error')
        except Exception as e:
            return False, str(e)

    # Auth Flow
    if not st.session_state["signedout"]:
        choice = st.radio('🔐 Login or Signup', ['Login', 'Sign up'], horizontal=True)

        email = st.text_input('📧 Email Address')
        password = st.text_input('🔑 Password', type='password')

        st.session_state.email_input = email
        st.session_state.password_input = password

        if choice == 'Sign up':
            username = st.text_input("🧑 Username")

            if st.button('🚀 Create my account'):
                if not username or not email or not password:
                    st.warning("⚠️ All fields are required.")
                elif not is_valid_email(email):
                    st.warning("📧 Please enter a valid email address.")
                elif not is_strong_password(password):
                    st.warning("🔐 Password must be at least 8 characters long and include:\n- Uppercase\n- Lowercase\n- Number\n- Special character")
                else:
                    user = sign_up_with_email_and_password(email=email, password=password, username=username)
                    st.success('✅ Account created successfully! Please login.')
                    st.balloons()
        else:
            if st.button('🔓 Login'):
                try:
                    userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
                    st.session_state.username = userinfo['username']
                    st.session_state.useremail = userinfo['email']
                    st.session_state.signedout = True
                    st.session_state.signout = True
                    st.success(f"✅ Welcome back, {userinfo['username'] or 'User'}!")
                except:
                    st.warning('❌ Login Failed. Please check your credentials.')

            with st.expander("Forgot Password?"):
                email_reset = st.text_input('Enter your email for password reset')
                if st.button("📩 Send Reset Link"):
                    if not is_valid_email(email_reset):
                        st.warning("⚠️ Invalid email format.")
                    else:
                        success, message = reset_password(email_reset)
                        if success:
                            st.success("✅ Password reset email sent.")
                        else:
                            st.error(f"❌ Failed: {message}")
