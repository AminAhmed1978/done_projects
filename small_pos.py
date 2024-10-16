import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Initialize session state for inventory and sales if not already initialized
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Item', 'Stock Qty', 'Purchase Rate', 'Selling Rate'])
if 'sales' not in st.session_state:
    st.session_state.sales = pd.DataFrame(columns=['Item', 'Qty', 'Rate', 'Amount'])

# Function to generate PDF bill with improved formatting
def generate_pdf_bill(sales_df, total_amount):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Invoice", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Item List", ln=True, align="L")

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Item | Qty | Rate | Amount", ln=True)
    pdf.cell(200, 5, txt="------------------------------------------", ln=True)

    for index, row in sales_df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Item']} | {row['Qty']} | {row['Rate']} | {row['Amount']}", ln=True)

    pdf.cell(200, 10, txt="------------------------------------------", ln=True)
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt=f"Total Amount: {total_amount}", ln=True)
    pdf.cell(200, 10, txt="------------------------------------------", ln=True)

    # Add footer text with developer information
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Developed by: AMIN AHMED", ln=True, align="C")

    pdf_file = "invoice.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Sidebar for navigation
st.sidebar.title("POS System")
st.sidebar.markdown("<h1 style='text-align: center; font-size: 24px;'>POS System</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='text-align: center; font-size: 15px;'>Developed by: AMIN AHMED</h2>", unsafe_allow_html=True)

selected_option = st.sidebar.radio("Choose an option:", ['Dashboard', 'Purchase Window', 'Selling Window', 'Stock'])

# Dashboard
if selected_option == 'Dashboard':
    # Add the main heading and developer information on the dashboard
    st.markdown("<h1 style='text-align: center; font-size: 32px;'>POS System</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-size: 15px;'>Developed by: AMIN AHMED</h2>", unsafe_allow_html=True)

    # Summarize and display total sales and profit
    total_sales = st.session_state.sales['Amount'].sum()
    total_profit = (st.session_state.sales['Amount'] - (st.session_state.sales['Qty'] * st.session_state.sales['Rate'])).sum()

    st.write(f"**Total Sales Amount:** ${total_sales:.2f}")
    st.write(f"**Total Profit Amount:** ${total_profit:.2f}")

    # Display a resized sales and profit bar chart
    if not st.session_state.sales.empty:
        fig, ax = plt.subplots(figsize=(6, 4))  # Reduced the chart size
        ax.bar(['Total Sales', 'Total Profit'], [total_sales, total_profit], color=['blue', 'green'])
        ax.set_title('Sales and Profit Summary')
        ax.set_ylabel('Amount ($)')
        st.pyplot(fig)
    else:
        st.write("No sales data available to display the graph.")

# Purchase Window using st.form
if selected_option == 'Purchase Window':
    st.title("Purchase Window")
    with st.form(key='purchase_form'):
        item = st.text_input("Item Name", key="item_name")
        stock_qty = st.number_input("Stock Quantity", min_value=0, step=1, key="stock_qty")
        purchase_rate = st.number_input("Purchase Rate", min_value=0.0, format="%.2f", key="purchase_rate")
        selling_rate = st.number_input("Selling Rate", min_value=0.0, format="%.2f", key="selling_rate")
        submit_button = st.form_submit_button(label="Add Item")

    if submit_button:
        new_item = {
            'Item': item,
            'Stock Qty': stock_qty,
            'Purchase Rate': purchase_rate,
            'Selling Rate': selling_rate
        }
        st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_item])], ignore_index=True)
        st.success(f"Added {item} to inventory.")
        # Clear form fields manually
        st.session_state.item_name = ""
        st.session_state.stock_qty = 0
        st.session_state.purchase_rate = 0.0
        st.session_state.selling_rate = 0.0

    st.write("Current Inventory")
    st.dataframe(st.session_state.inventory)

# Selling Window using st.form
if selected_option == 'Selling Window':
    st.title("Selling Window")
    with st.form(key='selling_form'):
        item_list = st.session_state.inventory['Item'].tolist()
        selected_item = st.selectbox("Select Item to Sell", item_list, key="selected_item")
        qty = st.number_input("Quantity", min_value=1, step=1, key="sell_qty")
        add_to_invoice_button = st.form_submit_button(label="Add to Invoice")

    if add_to_invoice_button and selected_item:
        rate = st.session_state.inventory.loc[st.session_state.inventory['Item'] == selected_item, 'Selling Rate'].values[0]
        amount = qty * rate

        sale_entry = {'Item': selected_item, 'Qty': qty, 'Rate': rate, 'Amount': amount}
        st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([sale_entry])], ignore_index=True)

        # Deduct sold quantity from stock
        st.session_state.inventory.loc[st.session_state.inventory['Item'] == selected_item, 'Stock Qty'] -= qty
        st.success(f"Added {selected_item} to invoice and updated inventory.")
        # Clear form fields manually
        st.session_state.sell_qty = 1

    st.write("Invoice")
    st.dataframe(st.session_state.sales)

    total_amount = st.session_state.sales['Amount'].sum()
    st.write(f"Total Amount: {total_amount}")

    if st.button("Generate Bill"):
        pdf_file = generate_pdf_bill(st.session_state.sales, total_amount)
        st.success("Bill generated successfully!")
        st.download_button("Download Invoice", data=open(pdf_file, "rb"), file_name="invoice.pdf", mime="application/pdf")

# Stock Information
if selected_option == 'Stock':
    st.title("Current Stock")
    st.write("Check remaining stock of items.")
    st.dataframe(st.session_state.inventory[['Item', 'Stock Qty']])
