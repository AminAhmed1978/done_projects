import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session states
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Item', 'Unit', 'Stock Qty', 'Purchase Rate', 'Selling Rate'])
if 'sales' not in st.session_state:
    st.session_state.sales = pd.DataFrame(columns=['Date', 'Item', 'Unit', 'Qty', 'Rate', 'Amount', 'Profit'])

# CSS styling
st.markdown("""
    <style>
    .main-title { text-align: center; color: #4CAF50; font-size: 32px; }
    .sub-title { text-align: center; color: #FF5733; font-size: 24px; }
    .footer-text { text-align: center; font-size: 14px; color: grey; }
    .button-container { text-align: center; margin: 20px; }
    </style>
""", unsafe_allow_html=True)

# Admin Login Function
def admin_login():
    st.markdown("<h1 class='main-title'>Admin Login</h1>", unsafe_allow_html=True)
    
    with st.form(key='admin_login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

    if login_button:
        if username == "admin" and password == "admin123":
            st.session_state.is_admin = True
            st.success("Admin login successful!")
        else:
            st.error("Incorrect username or password")

# Admin Dashboard
def admin_dashboard():
    st.markdown("<h1 class='main-title'>Admin Dashboard</h1>", unsafe_allow_html=True)
    total_sales = st.session_state.sales['Amount'].sum()
    total_profit = st.session_state.sales['Profit'].sum()

    st.write(f"**Total Sales Amount:** ${total_sales:.2f}")
    st.write(f"**Total Profit Amount:** ${total_profit:.2f}")

    if not st.session_state.sales.empty:
        st.dataframe(st.session_state.sales[['Date', 'Item', 'Unit', 'Qty', 'Rate', 'Amount', 'Profit']])
    else:
        st.write("No sales data available.")

# Inventory Management
def manage_inventory():
    st.markdown("<h1 class='sub-title'>Inventory Management</h1>", unsafe_allow_html=True)
    with st.form(key='inventory_form'):
        item = st.text_input("Item Name")
        unit = st.selectbox("Unit", ["Unit", "Kgs", "Dozen"])
        stock_qty = st.number_input("Stock Quantity", min_value=0, step=1)
        purchase_rate = st.number_input("Purchase Rate", min_value=0.0, format="%.2f")
        selling_rate = st.number_input("Selling Rate", min_value=0.0, format="%.2f")
        add_item_button = st.form_submit_button("Add Item")

    if add_item_button and item and unit:
        new_item = {
            'Item': item,
            'Unit': unit,
            'Stock Qty': stock_qty,
            'Purchase Rate': purchase_rate,
            'Selling Rate': selling_rate
        }
        st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_item])], ignore_index=True)
        st.success(f"Added {item} to inventory.")

    st.dataframe(st.session_state.inventory)

# Consumer Area
def consumer_area():
    st.markdown("<h1 class='sub-title'>Welcome to the POS System</h1>", unsafe_allow_html=True)
    
    with st.form(key='purchase_form'):
        item_list = st.session_state.inventory['Item'].tolist()
        selected_item = st.selectbox("Select Item to Buy", item_list)
        unit = st.selectbox("Unit", ["Unit", "Kgs", "Dozen"])
        qty = st.number_input("Quantity", min_value=1, step=1)
        purchase_button = st.form_submit_button("Add to Bill")

    if purchase_button and selected_item:
        rate = st.session_state.inventory[st.session_state.inventory['Item'] == selected_item]['Selling Rate'].values[0]
        purchase_rate = st.session_state.inventory[st.session_state.inventory['Item'] == selected_item]['Purchase Rate'].values[0]
        amount = qty * rate
        profit = qty * (rate - purchase_rate)
        sale_entry = {'Date': datetime.now().strftime('%Y-%m-%d'), 'Item': selected_item, 'Unit': unit, 'Qty': qty, 'Rate': rate, 'Amount': amount, 'Profit': profit}
        st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([sale_entry])], ignore_index=True)
        st.success(f"Added {selected_item} to bill.")

    st.write("### Current Bill Summary")
    if not st.session_state.sales.empty:
        st.dataframe(st.session_state.sales[['Item', 'Unit', 'Qty', 'Rate', 'Amount']])
    else:
        st.write("No items in the bill.")

# Main Navigation using Radio Buttons
st.sidebar.title("POS System Navigation")
role = st.sidebar.radio("Select your role:", ['Consumer', 'Admin'])

if role == 'Admin':
    if not st.session_state.is_admin:
        admin_login()
    else:
        admin_dashboard()
        manage_inventory()
else:
    consumer_area()

# Footer Information
st.markdown("<div class='footer-text'>Developed by: AMIN AHMED</div>", unsafe_allow_html=True)
