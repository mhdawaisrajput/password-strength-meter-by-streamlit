import re                   # Import regular expression module for pattern matching.
import random               # Import random module for generating random numbers.
import string               # Import string module for string operations.
import streamlit as st      # Import streamlit module for creating web app.

def suggest_password(length=8):
    """
    Generates a strong password that meets all criteria:
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character

    """
    # Ensure the password length is at least 8 characters if not, set it to 8
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


    # Expanded blacklist of common passwords
    common_passwords = {
        "password", "password123", "123456", "qwerty", "abc123", "111111",
        "12345678", "iloveyou", "admin", "welcome", "monkey", "login",
        "letmein", "princess", "dragon", "sunshine", "flower", "baseball",
        "football", "123123", "654321", "superman"
    }
    if password.lower() in common_passwords:
        print("❌ Password is too common. Please choose a less common password.")
        suggested = suggest_password()
        print("🔑 Suggested strong password:", suggested)
        return 

    # Check length
    if len(password) >= 8:
        # score += 1
        score += weight_length
    else:
        print("❌ Password must be 8 characters long")

    # Uppercase and lowercase letters check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        # score += 1
        score += weight_case
    else:
        print("❌ Password must contain at least one uppercase and one lowercase letter")

    # Check for digits
    if re.search(r"\d", password):
        score += weight_digit
    else:
        print("❌ Password must contain at least one digit")

    # Check for special characters
    if re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?~\\]", password):
        # score += 1
        score += weight_special
    else:
        print("❌ Password must contain at least one special character (!@#$%^&*()_+{}\\[\\]:;<>,.?~\\).")

    # Evaluate strength level based on weighted score

    print(f"Score: {score} out of {max_score}")  # <-- This line will display the score

    # if score == 4:
    if score == max_score:
        print("✅ Password is strong")

     # if score == 3:   
    elif score >= (max_score * 0.67):  # 67% or above is moderate
        print("⚠ Moderate Password; consider adding more security features.")
    else:
        print("❌ Password is weak; please improve it by following the instructions above.")
        suggested = suggest_password()
        print("🔑 Suggested strong password:", suggested)

# Test the function with a sample password
password = input("Enter your password: ")
password_strength_checker(password)