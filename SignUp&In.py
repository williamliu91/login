import streamlit as st
import pandas as pd
import os
import re

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

# Function to validate email address
def is_valid_email(email):
    # Basic regex for validating email addresses
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

# Function to validate password
def is_valid_password(password):
    # Check password length
    if len(password) < 6:
        return False
    
    # Check if password contains both letters and numbers
    has_letter = any(c.isalpha() for c in password)
    has_number = any(c.isdigit() for c in password)
    
    return has_letter and has_number

# Function to check if login credentials are valid
def validate_user(username, password):
    if os.path.isfile(CSV_FILE):
        data = pd.read_csv(CSV_FILE)

        # Convert columns to string type
        data['Username'] = data['Username'].astype(str).str.strip()
        data['Password'] = data['Password'].astype(str).str.strip()

        # Strip whitespace and compare in a case-insensitive way
        username = username.strip().lower()
        password = password.strip()

        # Match username and password (case-sensitive for password, case-insensitive for username)
        user_record = data[(data['Username'].str.lower() == username) & 
                           (data['Password'] == password)]

        return not user_record.empty
    return False

# Title of the sign-up page
st.title("Sign-Up Page")

# Page navigation options
page = st.sidebar.selectbox("Choose a page", ["Sign Up", "Login", "Admin"])

# Sign-up page
if page == "Sign Up":
    st.subheader("Create a new account")
    with st.form(key='signup_form'):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button(label='Sign Up')

        if submit_button:
            if username and email and password:
                if is_valid_email(email):
                    if is_valid_password(password):
                        save_to_csv(username, email, password)
                        st.success("You have successfully signed up!")
                    else:
                        st.error("Password must be at least 6 characters long and contain both letters and numbers.")
                else:
                    st.error("Invalid email address. Please enter a valid email.")
            else:
                st.error("Please fill out all fields.")

# Login page
if page == "Login":
    st.subheader("Login")
    with st.form(key='login_form'):
        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type='password')
        login_button = st.form_submit_button(label='Login')

        if login_button:
            if validate_user(login_username, login_password):
                st.success(f"Welcome, {login_username}!")
            else:
                st.error("Invalid username or password. Please try again.")

# Admin login form
if page == "Admin":
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
