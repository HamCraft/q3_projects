import streamlit as st  # Import Streamlit for UI
import random  # Import random for generating random choices
import string  # Import string for predefined character sets
from pyzxcvbn import zxcvbn  # Import zxcvbn for password strength analysis

# Function to generate a random password
def generate_password(length, use_digits, use_special):
    characters = string.ascii_letters  # Includes uppercase and lowercase letters

    if use_digits:
        characters += string.digits  # Adds numbers (0-9) if selected

    if use_special:
        characters += string.punctuation  # Adds special characters (!@#$%^&* etc.) if selected
    # Generate password by randomly selecting characters from the combined set
    return "".join(random.choice(characters) for _ in range(length))

# Function to check password strength
def check_password_strength(password):
    analysis = zxcvbn(password)
    score = analysis["score"]  # Strength score (0-4)
    feedback = analysis["feedback"]["suggestions"]

    # Convert numerical score to human-readable format
    strength_levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    strength_text = strength_levels[score]

    return strength_text, feedback

# Streamlit UI setup
st.title("Password Generator with Strength Meter")

# User input: password length
length = st.slider("Select password length:", min_value=6, max_value=32, value=12)

# Checkbox options for including numbers and special characters
use_digits = st.checkbox("Include numbers")
use_special = st.checkbox("Include special characters")

# Generate password button
if st.button("Generate Password"):
    password = generate_password(length, use_digits, use_special)
    st.write(f"**Generated Password:** `{password}`")

    # Analyze password strength
    strength_text, feedback = check_password_strength(password)
    st.write(f"**Strength:** {strength_text}")

    if feedback:
        st.write("**Suggestions to improve strength:**")
        for suggestion in feedback:
            st.write(f"- {suggestion}")

