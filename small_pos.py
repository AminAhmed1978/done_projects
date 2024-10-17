import streamlit as st
import pandas as pd

# CSS styles for a more professional look
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 36px;
            color: #4CAF50;
            font-weight: bold;
        }
        .sub-title {
            text-align: center;
            font-size: 24px;
            color: #4CAF50;
            font-weight: bold;
        }
        .info-text {
            color: #333;
            font-size: 16px;
            margin-top: 20px;
        }
        .dashboard-container {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }
        .dashboard-card {
            background-color: #f1f1f1;
            padding: 20px;
            border-radius: 10px;
            width: 45%;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .dashboard-card h3 {
            margin: 0;
            font-size: 24px;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for inventory, sales, and admin authentication
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Item', 'Unit', 'Stock Qty', 'Purchase Rate', 'Selling Rate'])
if 'sales' not in st.session_state:
    st.session_state.sales = pd.DataFrame(columns=['Item', 'Unit', 'Qty', 'Rate', 'Amount'])
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Admin authentication area
def admin_login():
    st.markdown("<h1 class='main-title'>Admin Login</h1>", unsafe_allow_html=True)
    username = st.text_input("Username", type="text")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.is_admin = True
            st.success("Admin login successful!")
        else:
            st.error("Incorrect username or password")

# Admin area with inventory management and dashboard
def admin_area():
    st.markdown("<h1 class='main-title'>Admin Area</h1>", unsafe_allow_html=True)

    # Dashboard for total sales and profit
    st.markdown("<h2 class='sub-title'>Dashboard</h2>", unsafe_allow_html=True)
    total_sales = st.session_state.sales['Amount'].sum()
    total_profit = (st.session_state.sales['Amount'] - (st.session_state.sales['Qty'] * st.session_state.sales['Rate'])).sum()

    st.markdown(f"""
        <div class='dashboard-container'>
            <div class='dashboard-card'>
                <h3>Total Sales Amount</h3>
                <p>${total_sales:,.2f}</p>
            </div>
            <div class='dashboard-card'>
                <h3>Total Profit Amount</h3>
                <p>${total_profit:,.2f}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Inventory management form
    st.markdown("<h2 class='sub-title'>Manage Inventory</h2>", unsafe_allow_html=True)
    with st.form(key='inventory_form'):
        item = st.text_input("Item Name")
        unit = st.selectbox("Unit", ["Unit", "Kgs", "Dozen"])
        stock_qty = st.number_input("Stock Quantity", min_value=0, step=1)
        purchase_rate = st.number_input("Purchase Rate", min_value=0.0, format="%.2f")
        selling_rate = st.number_input("Selling Rate", min_value=0.0, format="%.2f")
        submit_button = st.form_submit_button(label="Add Item")

    if submit_button:
        new_item = {
            'Item': item,
            'Unit': unit,
            'Stock Qty': stock_qty,
            'Purchase Rate': purchase_rate,
            'Selling Rate': selling_rate
        }
        st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_item])], ignore_index=True)
        st.success(f"Item '{item}' added to inventory.")

    # Display current inventory
    st.write("**Current Inventory**")
    st.dataframe(st.session_state.inventory)

# Customer area for making purchases
def customer_area():
    st.markdown("<h1 class='main-title'>Customer Area</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-title'>Make a Purchase</h2>", unsafe_allow_html=True)

    if not st.session_state.inventory.empty:
        with st.form(key='sales_form'):
            item_list = st.session_state.inventory['Item'].tolist()
            selected_item = st.selectbox("Select Item", item_list)
            unit = st.selectbox("Unit", ["Unit", "Kgs", "Dozen"])
            qty = st.number_input("Quantity", min_value=1, step=1)
            add_to_invoice_button = st.form_submit_button(label="Add to Invoice")

        if add_to_invoice_button:
            rate = st.session_state.inventory[st.session_state.inventory['Item'] == selected_item]['Selling Rate'].values[0]
            amount = qty * rate
            sale_entry = {'Item': selected_item, 'Unit': unit, 'Qty': qty, 'Rate': rate, 'Amount': amount}
            st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([sale_entry])], ignore_index=True)
            st.success(f"Item '{selected_item}' added to the invoice.")

        # Display sales invoice
        st.markdown("<h3 class='sub-title'>Sales Invoice</h3>", unsafe_allow_html=True)
        if not st.session_state.sales.empty:
            st.dataframe(st.session_state.sales)
            st.write(f"**Total Amount Due:** ${st.session_state.sales['Amount'].sum():,.2f}")
    else:
        st.warning("No items available for sale. Please check back later.")

# Main app logic to switch between admin and customer areas
st.sidebar.title("POS System Navigation")
user_type = st.sidebar.radio("Choose your role:", ["Admin", "Customer"])

if user_type == "Admin":
    if st.session_state.is_admin:
        admin_area()
    else:
        admin_login()
else:
    customer_area()
