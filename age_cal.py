import streamlit as st
from datetime import datetime, date

# Function to calculate age and horoscope
def calculate_age_and_horoscope(birth_date):
    today = date.today()
    age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    age_days = (today - birth_date).days

    horoscope_sign = get_horoscope(birth_date)

    return age_years, age_days, horoscope_sign

# Function to determine horoscope based on date of birth
def get_horoscope(birth_date):
    month = birth_date.month
    day = birth_date.day

    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"

# Streamlit UI setup
st.title("Age Calculator")

# Creating a calculator-like input area
st.markdown("<h3 style='text-align: center;'>Enter Your Details</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.write("")  # Empty space for better alignment

with col2:
    name = st.text_input("Name:", "")
    gender = st.radio("Gender:", ["Male", "Female", "Other"])
    dob = st.date_input("Date of Birth:")

    # Adding calculator-like buttons
    if st.button("Calculate Age"):
        if name and dob:
            age_years, age_days, horoscope = calculate_age_and_horoscope(dob)
            st.success("Result:")
            st.write(f"**Name**: {name}")
            st.write(f"**Gender**: {gender}")
            st.write(f"**Age**: {age_years} years")
            st.write(f"**Age in Days**: {age_days} days")
            st.write(f"**Horoscope Sign**: {horoscope}")
        else:
            st.warning("Please enter your complete details.")

with col3:
    st.write("")  # Empty space for better alignment

# Styling the calculator-like appearance
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #4CAF50; /* Green background */
        color: white; /* White text */
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border: none;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True
)
