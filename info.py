import streamlit as st

def app():
    st.markdown("<h1 style='color:	#DC143C;'>👤 Account Details</h1>", unsafe_allow_html=True)
    
    if not st.session_state.get("signedout"):
        st.warning("⚠️ Please login first.")
        st.stop()
    
    st.write(f"**👤 Name:** {st.session_state.username}")
    st.write(f"**📧 Email:** {st.session_state.useremail}")

    if st.button("🚪 Sign out"):
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''
        st.session_state.useremail = ''
        st.success("You have been signed out.")

   
   