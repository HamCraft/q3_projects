import streamlit as st
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import json

# File to store user data
DATA_FILE = "users.json"

# Load users from JSON file
def load_users():
    """Load user data from users.json. Return empty dict if file doesn't exist."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save users to JSON file
def save_users(users):
    """Save user data to users.json."""
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f)

# Generate encryption key from passkey and salt
def generate_key(passkey, salt):
    """Derive a Fernet-compatible key using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passkey.encode()))
    return key

# Encrypt data
def encrypt_data(data, passkey, salt):
    """Encrypt data with a key derived from passkey and salt."""
    key = generate_key(passkey, salt)
    f = Fernet(key)
    return f.encrypt(data.encode())

# Decrypt data
def decrypt_data(encrypted_data, passkey, salt):
    """Decrypt data with a key derived from passkey and salt."""
    key = generate_key(passkey, salt)
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()

# Register a new user
def register_user(username, password):
    """Register a new user with hashed password and salt."""
    users = load_users()
    if username in users:
        return False  # Username taken
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    password_hash = kdf.derive(password.encode())
    users[username] = {
        'password_hash': base64.b64encode(password_hash).decode(),
        'salt': base64.b64encode(salt).decode(),
        'data': []
    }
    save_users(users)
    return True

# Authenticate user login
def login_user(username, password):
    """Verify user credentials."""
    users = load_users()
    if username not in users:
        return False
    user = users[username]
    salt = base64.b64decode(user['salt'])
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    password_hash = kdf.derive(password.encode())
    stored_hash = base64.b64decode(user['password_hash'])
    return password_hash == stored_hash

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

# Login and Registration Page
def login_page():
    st.title("Login or Register")
    option = st.radio("Choose:", ["Login", "Register"])
    
    if option == "Register":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            if register_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Registered and logged in successfully!")
                st.rerun()
            else:
                st.error("Username already exists")
    else:  # Login
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.attempts = 0
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Incorrect username or password")

# Insert Data Page
def insert_data_page():
    st.title("Store Secure Data")
    data = st.text_area("Enter data to encrypt")
    passkey = st.text_input("Enter passkey", type="password")
    if st.button("Store Data"):
        if data and passkey:
            salt = os.urandom(16)
            encrypted_text = encrypt_data(data, passkey, salt)
            encrypted_text_b64 = base64.b64encode(encrypted_text).decode()
            salt_b64 = base64.b64encode(salt).decode()
            users = load_users()
            user_data = users[st.session_state.username]['data']
            user_data.append({"encrypted_text": encrypted_text_b64, "salt": salt_b64})
            save_users(users)
            st.success("Data stored successfully")
        else:
            st.error("Please provide both data and passkey")

# Retrieve Data Page
def retrieve_data_page():
    st.title("Retrieve Secure Data")
    users = load_users()
    user_data = users[st.session_state.username]['data']
    if not user_data:
        st.warning("No data stored yet.")
    else:
        data_ids = [f"Data {i+1}" for i in range(len(user_data))]
        selected_id = st.selectbox("Select data to retrieve", data_ids)
        index = data_ids.index(selected_id)
        passkey = st.text_input("Enter passkey", type="password")
        st.write(f"Failed attempts: {st.session_state.attempts}/3")
        if st.button("Decrypt Data"):
            if passkey:
                encrypted_text_b64 = user_data[index]['encrypted_text']
                salt_b64 = user_data[index]['salt']
                encrypted_text = base64.b64decode(encrypted_text_b64)
                salt = base64.b64decode(salt_b64)
                try:
                    decrypted_text = decrypt_data(encrypted_text, passkey, salt)
                    st.success("Decryption successful!")
                    st.write("Decrypted data:", decrypted_text)
                    st.session_state.attempts = 0
                except:
                    st.session_state.attempts += 1
                    st.error("Incorrect passkey")
                    if st.session_state.attempts >= 3:
                        st.session_state.authenticated = False
                        st.warning("Too many failed attempts. Please log in again.")
                        st.rerun()
            else:
                st.error("Please provide a passkey")

# Home Page
def home_page():
    st.title("Secure Data Encryption System")
    option = st.radio("Choose an option:", ["Store New Data", "Retrieve Data"])
    if option == "Store New Data":
        insert_data_page()
    else:
        retrieve_data_page()

# Main app logic
def main():
    if st.session_state.authenticated:
        home_page()
    else:
        login_page()

if __name__ == "__main__":
    st.set_page_config(page_title="Secure Data System", layout="wide")
    main()