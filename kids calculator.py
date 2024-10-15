import streamlit as st

# Conversion functions
def cm_to_feet_inches(cm):
    inches = cm / 2.54
    feet = int(inches // 12)
    remaining_inches = int(inches % 12)
    return f"{feet} ft {remaining_inches} in"

def kg_to_lbs(kg):
    return round(kg * 2.20462, 1)

# Function to get height and weight ranges based on age and gender
def get_kid_growth_ranges(age, gender):
    ranges = {
        'Male': {
            1: (71, 83, 8.6, 12), 2: (80, 91, 10, 14.5),
            3: (86, 99, 11.5, 16.5), 4: (92, 105, 12.5, 18),
            5: (98, 112, 14, 21), 6: (104, 118, 16, 24),
            7: (109, 124, 18, 27), 8: (114, 130, 20, 30)
        },
        'Female': {
            1: (70, 81, 8, 11.5), 2: (78, 90, 9.5, 13.5),
            3: (85, 98, 11, 16), 4: (91, 105, 12, 18),
            5: (97, 112, 13.5, 20), 6: (103, 118, 15.5, 23),
            7: (108, 125, 17.5, 26), 8: (113, 131, 19, 29)
        }
    }
    return ranges.get(gender, {}).get(age, (None, None, None, None))

# Streamlit app UI
st.title("Child Height and Weight Calculator")

# Get user input for age and gender
age = st.number_input("Enter age of the child (1-8 years):", min_value=1, max_value=8, step=1)
gender = st.selectbox("Select the child's gender:", ["Male", "Female"])

# Display recommended height and weight range
if st.button("Calculate"):
    min_height, max_height, min_weight, max_weight = get_kid_growth_ranges(age, gender)
    if min_height:
        st.write(f"Recommended Height Range: {min_height}-{max_height} cm ({cm_to_feet_inches(min_height)} - {cm_to_feet_inches(max_height)})")
        st.write(f"Recommended Weight Range: {min_weight}-{max_weight} kg ({kg_to_lbs(min_weight)}-{kg_to_lbs(max_weight)} lbs)")
    else:
        st.write("Data not available for the specified age and gender.")
