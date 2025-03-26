import re           # Import regular expression module for pattern matching.
import random       # Import random module for generating random numbers.
import string       # Import string module for string operations.
import streamlit as st  # Import streamlit for UI

def suggest_password(length=8):
    """
    Generates a strong password that meets all criteria:
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if length < 8:
        length = 8

    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*()_+{}\\[\\]:;<>,.?~\\")
    
    remaining_length = length - 4
    all_characters = string.ascii_letters + string.digits + "!@#$%^&*()_+{}\\[\\]:;<>,.?~\\"
    remaining_password = ''.join(random.choice(all_characters) for _ in range(remaining_length))
    
    password_list = list(uppercase + lowercase + digit + special + remaining_password)
    random.shuffle(password_list)
    return ''.join(password_list)

def password_strength_checker(password):
    score = 0
    
    # Custom scoring weights
    weight_length = 2        # Weight for minimum length (8 or more)
    weight_case = 2          # Weight for uppercase and lowercase letters
    weight_digit = 1         # Weight for digits
    weight_special = 1       # Weight for special characters
    max_score = weight_length + weight_case + weight_digit + weight_special  # max score = 6

    messages = []

    # Expanded blacklist of common passwords
    common_passwords = {
        "password", "password123", "123456", "qwerty", "abc123", "111111",
        "12345678", "iloveyou", "admin", "welcome", "monkey", "login",
        "letmein", "princess", "dragon", "sunshine", "flower", "baseball",
        "football", "123123", "654321", "superman"
    }
    if password.lower() in common_passwords:
        messages.append("❌ Password is too common. Please choose a less common password. 🚫")
        suggested = suggest_password()
        messages.append("🔑 Suggested Strong Password: " + suggested + " 💡")
        return score, max_score, messages
    
    

    # Check length
    if len(password) >= 8:
        score += weight_length
    else:
        messages.append("❌ Password must be 8 characters long. ⏱️")

    # Check for uppercase and lowercase letters
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += weight_case
    else:
        messages.append("❌ Password must contain at least one uppercase and one lowercase letter. 🔠")

    # Check for digits
    if re.search(r"\d", password):
        score += weight_digit
    else:
        messages.append("❌ Password must contain at least one digit. 🔢")

    # Check for special characters
    if re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?~\\]", password):
        score += weight_special
    else:
        messages.append("❌ Password must contain at least one special character (!@#$%^&*()_+{}\\[\\]:;<>,.?~\\). ✨")
        
    messages.append(f"📊 Score: {score} out of {max_score}")
    
    if score == max_score:
         messages.append(f"✅ Password is strong! 💪")
    elif score >= (max_score * 0.67):  # 67% or above is moderate
        messages.append("⚠ Moderate Password; consider adding more security features. 🤔")
    else:
        messages.append("❌ Password is weak; please improve it by following the instructions above. 🛠️")
        suggested = suggest_password()
        messages.append("🔑 Suggested Strong Password: " + suggested + " 💡")
        

    return score, max_score, messages

# Streamlit UI
st.title("🔒 Password Strength Checker")
password = st.text_input("Enter your password:", type="password")

# Create two columns for the buttons
col1, col2 = st.columns(2)
with col1:
    check_button = st.button("🔍 Check Password")
with col2:
    suggest_button = st.button("💡 Generate Suggested Password")

if check_button:
    if password:
        score, max_score, messages = password_strength_checker(password)
        for msg in messages:
            st.write(msg)
    else:
        st.write("🚫 Please enter a password.")

if suggest_button:
    suggested = suggest_password()
    st.write("🔑 Suggested Strong Password: " + suggested + " 💡" )


# --- Terminal Test Code ---
# The following lines are for testing via terminal.
# When running as a Streamlit app, these lines should be commented out or removed.
# password = input("Enter your password: ")
# password_strength_checker(password)