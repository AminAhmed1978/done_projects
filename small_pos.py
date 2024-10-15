import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Initialize session state for inventory and sales if not already initialized
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Item', 'Stock Qty', 'Purchase Rate', 'Selling Rate'])
if 'sales' not in st.session_state:
    st.session_state.sales = pd.DataFrame(columns=['Item', 'Qty', 'Rate', 'Amount', 'Profit'])

# Function to generate PDF bill
def generate_pdf_bill(sales_df, total_amount):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Invoice", ln=True, align="C")
    pdf.cell(200, 10, txt="Item List", ln=True, align="L")

    for index, row in sales_df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Item']} | Qty: {row['Qty']} | Rate: {row['Rate']} | Amount: {row['Amount']} | Profit: {row['Profit']}", ln=True)

    pdf.cell(200, 10, txt=f"Total Amount: {total_amount}", ln=True)
    pdf_file = "invoice.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Main Dashboard with Graph
st.sidebar.title("POS System")
if st.sidebar.button("Dashboard"):
    st.title("Sales and Profit Dashboard")
    if not st.session_state.sales.empty:
        fig, ax = plt.subplots()
        ax.bar(st.session_state.sales['Item'], st.session_state.sales['Amount'], label='Sales Amount', color='blue')
        ax.bar(st.session_state.sales['Item'], st.session_state.sales['Profit'], label='Profit Amount', color='green')
        ax.set_xlabel('Items')
        ax.set_ylabel('Amount')
        ax.set_title('Sales and Profit Visualization')
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("No sales data available to display the graph.")

# Purchase Window using st.form
if st.sidebar.button("Purchase Window"):
    st.title("Purchase Window")
    with st.form(key='purchase_form'):
        item = st.text_input("Item Name", key="item_name")
        stock_qty = st.number_input("Stock Quantity", min_value=0, step=1, key="stock_qty")
        purchase_rate = st.number_input("Purchase Rate", min_value=0.0, format="%.2f", key="purchase_rate")
        selling_rate = st.number_input("Selling Rate", min_value=0.0, format="%.2f", key="selling_rate")
        submit_button = st.form_submit_button(label="Add Item")

    if submit_button:
        new_item = {
            'Item': st.session_state.item_name,
            'Stock Qty': st.session_state.stock_qty,
            'Purchase Rate': st.session_state.purchase_rate,
            'Selling Rate': st.session_state.selling_rate
        }
        st.session_state.inventory = st.session_state.inventory.append(new_item, ignore_index=True)
        st.success(f"Added {st.session_state.item_name} to inventory.")

    st.write("Current Inventory")
    st.dataframe(st.session_state.inventory)

# Selling Window using st.form
if st.sidebar.button("Selling Window"):
    st.title("Selling Window")
    with st.form(key='selling_form'):
        item_list = st.session_state.inventory['Item'].tolist()
        selected_item = st.selectbox("Select Item to Sell", item_list, key="selected_item")
        qty = st.number_input("Quantity", min_value=1, step=1, key="sell_qty")
        add_to_invoice_button = st.form_submit_button(label="Add to Invoice")

    if add_to_invoice_button and selected_item:
        rate = st.session_state.inventory[st.session_state.inventory['Item'] == selected_item]['Selling Rate'].values[0]
        purchase_rate = st.session_state.inventory[st.session_state.inventory['Item'] == selected_item]['Purchase Rate'].values[0]
        amount = st.session_state.sell_qty * rate
        profit = st.session_state.sell_qty * (rate - purchase_rate)

        sale_entry = {'Item': selected_item, 'Qty': st.session_state.sell_qty, 'Rate': rate, 'Amount': amount, 'Profit': profit}
        st.session_state.sales = st.session_state.sales.append(sale_entry, ignore_index=True)
        st.success(f"Added {selected_item} to invoice.")

    st.write("Invoice")
    st.dataframe(st.session_state.sales)

    total_amount = st.session_state.sales['Amount'].sum()
    st.write(f"Total Amount: {total_amount}")

    if st.button("Generate Bill"):
        pdf_file = generate_pdf_bill(st.session_state.sales, total_amount)
        st.success("Bill generated successfully!")
        st.download_button("Download Invoice", data=open(pdf_file, "rb"), file_name="invoice.pdf", mime="application/pdf")
