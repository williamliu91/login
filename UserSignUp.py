import streamlit as st
import pandas as pd
import os

# File path for storing user data
CSV_FILE = 'user_data.csv'

# Hardcoded admin credentials (For demonstration purposes only; use environment variables or a secure method in production)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

# Function to save user data to CSV
def save_to_csv(username, email, password):
    if os.path.isfile(CSV_FILE):
        data = pd.DataFrame({
            'Username': [username],
            'Email': [email],
            'Password': [password]
        })
        data.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        data = pd.DataFrame({
            'Username': [username],
            'Email': [email],
            'Password': [password]
        })
        data.to_csv(CSV_FILE, mode='w', header=True, index=False)

# Title of the sign-up page
st.title("Sign-Up Page")

# Collect user input for sign-up
with st.form(key='signup_form'):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    submit_button = st.form_submit_button(label='Sign Up')

    if submit_button:
        if username and email and password:
            save_to_csv(username, email, password)
            st.success("You have successfully signed up!")
        else:
            st.error("Please fill out all fields.")

# Admin login form
st.sidebar.title("Admin Login")
admin_username = st.sidebar.text_input("Admin Username")
admin_password = st.sidebar.text_input("Admin Password", type='password')

# Check if admin credentials are correct
if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
    st.sidebar.success("Admin logged in")

    # Display CSV contents
    if os.path.isfile(CSV_FILE):
        st.subheader("User Data")
        data = pd.read_csv(CSV_FILE)
        st.write(data)
else:
    st.sidebar.warning("Please log in as admin to view user data.")
