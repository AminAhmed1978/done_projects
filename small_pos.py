import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Initialize session state for inventory and sales if not already initialized
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Item', 'Stock Qty', 'Purchase Rate', 'Selling Rate'])
if 'sales' not in st.session_state:
    st.session_state.sales = pd.DataFrame(columns=['Item', 'Qty', 'Rate', 'Amount'])

# Function to generate a more formatted PDF bill
def generate_pdf_bill(sales_df, total_amount):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="POS System", ln=True, align="C")
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(200, 10, txt="Developed by: AMIN AHMED", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Invoice", ln=True, align="L")
    pdf.ln(5)

    for index, row in sales_df.iterrows():
        pdf.cell(200, 10, txt=f"Item: {row['Item']} | Qty: {row['Qty']} | Rate: {row['Rate']} | Amount: {row['Amount']}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total Amount: {total_amount}", ln=True)
    pdf.cell(200, 10, txt="Thank you for your purchase!", ln=True)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Developed by: AMIN AHMED", ln=True, align="C")
    pdf_file = "invoice.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Main Dashboard with Graph
st.title("POS System")
st.subheader("Developed by: AMIN AHMED")

st.sidebar.title("Navigation")
selected_option = st.sidebar.radio("Choose an option:", ['Dashboard', 'Purchase Window', 'Selling Window', 'Stock'])

# Dashboard
if selected_option == 'Dashboard':
    st.header("Sales and Profit Dashboard")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Purchase Invoice")
    with col2:
        st.button("Sales Invoice")

    if not st.session_state.sales.empty:
        total_sales = st.session_state.sales['Amount'].sum()
        total_profit = (st.session_state.sales['Amount'] - 
                        st.session_state.sales['Qty'] * st.session_state.inventory['Purchase Rate']).sum()

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(['Total Sales', 'Total Profit'], [total_sales, total_profit], color=['blue', 'green'])
        ax.set_title('Sales and Profit Overview')
        ax.set_ylabel('Amount')
        st.pyplot(fig)
    else:
        st.write("No sales data available to display the graph.")

# Purchase Window
if selected_option == 'Purchase Window':
    st.header("Purchase Window")
    with st.form(key='purchase_form'):
        item_name = st.text_input("Item Name")
        stock_qty = st.number_input("Stock Quantity", min_value=0, step=1)
        purchase_rate = st.number_input("Purchase Rate", min_value=0.0, format="%.2f")
        selling_rate = st.number_input("Selling Rate", min_value=0.0, format="%.2f")
        submit_button = st.form_submit_button(label="Add Item")

    if submit_button:
        new_item = {'Item': item_name, 'Stock Qty': stock_qty, 'Purchase Rate': purchase_rate, 'Selling Rate': selling_rate}
        st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_item])], ignore_index=True)
        st.success(f"Added {item_name} to inventory.")
        # Clear fields
        st.experimental_rerun()

# Selling Window
if selected_option == 'Selling Window':
    st.header("Selling Window")
    with st.form(key='selling_form'):
        item_list = st.session_state.inventory['Item'].tolist()
        selected_item = st.selectbox("Select Item to Sell", item_list)
        qty = st.number_input("Quantity", min_value=1, step=1)
        add_to_invoice_button = st.form_submit_button(label="Add to Invoice")

    if add_to_invoice_button and selected_item:
        item_data = st.session_state.inventory[st.session_state.inventory['Item'] == selected_item]
        rate = item_data['Selling Rate'].values[0]
        purchase_rate = item_data['Purchase Rate'].values[0]
        amount = qty * rate

        sale_entry = {'Item': selected_item, 'Qty': qty, 'Rate': rate, 'Amount': amount}
        st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([sale_entry])], ignore_index=True)

        # Update stock quantity
        st.session_state.inventory.loc[st.session_state.inventory['Item'] == selected_item, 'Stock Qty'] -= qty
        st.success(f"Added {selected_item} to invoice.")
        st.experimental_rerun()

    st.write("Invoice")
    st.dataframe(st.session_state.sales)

    total_amount = st.session_state.sales['Amount'].sum()
    st.write(f"Total Amount: {total_amount}")

    if st.button("Generate Bill"):
        pdf_file = generate_pdf_bill(st.session_state.sales, total_amount)
        st.success("Bill generated successfully!")
        st.download_button("Download Invoice", data=open(pdf_file, "rb"), file_name="invoice.pdf", mime="application/pdf")

# Stock Window
if selected_option == 'Stock':
    st.header("Current Stock Levels")
    st.dataframe(st.session_state.inventory)
