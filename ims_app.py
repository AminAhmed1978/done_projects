import streamlit as st

# Initialize session state for login status
if 'management_password_verified' not in st.session_state:
    st.session_state.management_password_verified = False
if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
if 'user_access_level' not in st.session_state:
    st.session_state.user_access_level = None

# Function to handle user authentication
def user_authentication(limited_access=False):
    user_ids = ["ADMIN", "USER"]
    selected_user = st.selectbox("Select User ID", user_ids)
    user_password = st.text_input("Enter User Password:", type="password")

    if st.button("Login", key="user_login_button"):
        if selected_user == "ADMIN" and user_password == "admin_pass":
            st.session_state.user_logged_in = True
            st.session_state.user_access_level = "ADMIN" if not limited_access else "LIMITED_ADMIN"
            st.success("Admin Access Granted!")
        elif selected_user == "USER" and user_password == "user_pass":
            st.session_state.user_logged_in = True
            st.session_state.user_access_level = "USER"
            st.success("User Access Granted!")
        else:
            st.error("Incorrect User ID or Password! System Closed.")
            st.stop()

# Function to display the Windows-like menu using Streamlit's expanders
def display_menu():
    st.sidebar.title("Menu")

    with st.sidebar.expander("REGISTRATION"):
        st.write("- USER CODES")
        st.write("- USER OPTIONS")
        st.write("- COMPANY CODE")
        st.write("- GODOWN CODE")
        st.write("- ITEM CODES")
        st.write("- SUPPLIER/DISTRIBUTORS")
        st.write("- AREA")
        st.write("- SALES MAN")
        st.write("- CUSTOMER REG/LIMIT CHANGE")
        st.write("- PARTY CODE")

    with st.sidebar.expander("TRANSACTION"):
        st.write("- EXPENSE CODES")
        st.write("- BANK CODE")
        st.write("- PERSONAL DRAWING CODES")
        st.write("- LOAN ACCOUNTS CODE")
        st.write("- ASSETS CODES")
        st.write("- CAPITAL A/C")

    with st.sidebar.expander("CORRECTION"):
        st.write("- Correction Options")

    with st.sidebar.expander("REPORTS"):
        st.write("- Reports Options")

    with st.sidebar.expander("PRINTING/PDF"):
        st.write("- Printing Options")

    with st.sidebar.expander("OTHERS/SETTINGS"):
        st.write("- Other Settings")

# Function to display the dashboard
def display_dashboard():
    st.subheader("Dashboard Overview")
    st.info("Graph placeholders will be here for sales, costs, and profits.")

# Main Logic
if not st.session_state.management_password_verified:
    # Step 1: Management Password Entry
    management_password_input = st.text_input("Enter Management Password:", type="password")
    if st.button("Submit Management Password", key="management_login_button"):
        if management_password_input == "admin123":
            st.session_state.management_password_verified = True
            st.success("Management Password Verified!")
        else:
            st.error("Incorrect Management Password! Proceeding to limited access.")
            user_authentication(limited_access=True)
else:
    # Step 2: User Authentication
    if not st.session_state.user_logged_in:
        user_authentication()
    else:
        # Step 3: Display dashboard and menu after successful login
        display_dashboard()
        display_menu()
