import streamlit as st
import streamlit.components.v1 as components

# CSS styling for the menu bar (similar to the one you provided)
menu_css = """
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #111111;
        color: white;
    }

    .menu-bar {
        background-color: #333;
        overflow: hidden;
        padding: 10px;
    }

    .menu-bar a {
        float: left;
        color: #f2f2f2;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
        font-size: 17px;
    }

    .menu-bar a:hover {
        background-color: #ddd;
        color: black;
    }

    .dropdown {
        float: left;
        overflow: hidden;
    }

    .dropdown .dropbtn {
        font-size: 17px;
        border: none;
        outline: none;
        color: white;
        padding: 14px 16px;
        background-color: inherit;
        font-family: inherit;
        margin: 0;
    }

    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f9f9f9;
        min-width: 160px;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
        z-index: 1;
    }

    .dropdown-content a {
        float: none;
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
        text-align: left;
    }

    .dropdown-content a:hover {
        background-color: #ddd;
    }

    .dropdown:hover .dropdown-content {
        display: block;
    }

    .dashboard {
        padding: 20px;
        text-align: center;
        background-color: #444;
        margin-top: 20px;
    }
</style>
"""

# HTML structure for the menu bar
menu_html = """
<div class="menu-bar">
            <div class="dropdown">
                <a href="#">REGISTRATION</a>
                <div class="dropdown-content">
                    <a href="#">USER CODES</a>
                    <a href="#">USER OPTIONS</a>
                    <a href="#">COMPANY CODE</a>
                    <a href="#">GODOWN CODE</a>
                    <a href="#">ITEM CODES</a>
                    <a href="#">SUPPLIER/DISTRIBUTORS</a>
                    <a href="#">AREA</a>
                    <a href="#">SALES MAN</a>
                    <a href="#">CUSTOMER REG/LIMIT CHANGE</a>
                    <a href="#">PARTY CODE</a>
                </div>
            </div>
            <div class="dropdown">
                <a href="#">TRANSACTION</a>
                <div class="dropdown-content">
                    <a href="#">EXPENSE CODES</a>
                    <a href="#">BANK CODE</a>
                    <a href="#">PERSONAL DRAWING CODES</a>
                    <a href="#">LOAN ACCOUNTS CODE</a>
                    <a href="#">ASSETS CODES</a>
                    <a href="#">CAPITAL A/C</a>
                </div>
            </div>
            <div class="dropdown">
                <a href="#">CORRECTION</a>
            </div>
            <div class="dropdown">
                <a href="#">REPORTS</a>
            </div>
            <div class="dropdown">
                <a href="#">PRINTING/PDF</a>
            </div>
            <div class="dropdown">
                <a href="#">OTHERS/SETTINGS</a>
            </div>
        </div>
 """  

# Function to handle user authentication
def user_authentication(limited_access=False):
    user_ids = ["ADMIN", "USER"]
    selected_user = st.selectbox("Select User ID", user_ids)
    user_password = st.text_input("Enter User Password:", type="password")

    if st.button("Login"):
        if selected_user == "ADMIN" and user_password == "admin_pass":
            if limited_access:
                st.warning("Limited Admin Access due to incorrect management password!")
            else:
                st.success("Full Admin Access Granted!")
            display_dashboard(full_access=True)
        elif selected_user == "USER" and user_password == "user_pass":
            st.success("User Access Granted with Limited Rights!")
            display_dashboard(full_access=False)
        else:
            st.error("Incorrect User ID or Password! System Closed.")
            st.stop()

# Function to display the dashboard
def display_dashboard(full_access):
    st.subheader("Dashboard Overview")
    # Placeholder for graph logic (could use matplotlib or Plotly)
    st.info("Graph placeholders will be here for sales, costs, and profits.")
    
    components.html(menu_html, height=250)
    st.markdown(menu_css, unsafe_allow_html=True)

# Main
management_password = "admin123"
management_password_input = st.text_input("Enter Management Password:", type="password")

if st.button("Login"):
    if management_password_input == management_password:
        st.success("Management Password Verified!")
        user_authentication()
    else:
        st.error("Incorrect Management Password! Proceeding to limited access.")
        user_authentication(limited_access=True)

# Display menu
components.html(menu_html, height=250)
st.markdown(menu_css, unsafe_allow_html=True)
