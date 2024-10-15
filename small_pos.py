import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# DataFrame to hold purchase and sale items
inventory = pd.DataFrame(columns=['Item', 'Stock Qty', 'Purchase Rate', 'Selling Rate'])
sales = pd.DataFrame(columns=['Item', 'Qty', 'Rate', 'Amount', 'Profit'])

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
    if not sales.empty:
        fig, ax = plt.subplots()
        ax.bar(sales['Item'], sales['Amount'], label='Sales Amount', color='blue')
        ax.bar(sales['Item'], sales['Profit'], label='Profit Amount', color='green')
        ax.set_xlabel('Items')
        ax.set_ylabel('Amount')
        ax.set_title('Sales and Profit Visualization')
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("No sales data available to display the graph.")

# Purchase Window
if st.sidebar.button("Purchase Window"):
    st.title("Purchase Window")
    item = st.text_input("Item Name")
    stock_qty = st.number_input("Stock Quantity", min_value=0, step=1)
    purchase_rate = st.number_input("Purchase Rate", min_value=0.0, format="%.2f")
    selling_rate = st.number_input("Selling Rate", min_value=0.0, format="%.2f")

    if st.button("Add Item"):
        inventory = inventory.append({'Item': item, 'Stock Qty': stock_qty, 'Purchase Rate': purchase_rate, 'Selling Rate': selling_rate}, ignore_index=True)
        st.success(f"Added {item} to inventory.")

    st.write("Current Inventory")
    st.dataframe(inventory)

# Selling Window
if st.sidebar.button("Selling Window"):
    st.title("Selling Window")
    item_list = inventory['Item'].tolist()
    selected_item = st.selectbox("Select Item to Sell", item_list)
    qty = st.number_input("Quantity", min_value=1, step=1)
    
    if selected_item:
        rate = inventory[inventory['Item'] == selected_item]['Selling Rate'].values[0]
        purchase_rate = inventory[inventory['Item'] == selected_item]['Purchase Rate'].values[0]
        amount = qty * rate
        profit = qty * (rate - purchase_rate)

        if st.button("Add to Invoice"):
            sales = sales.append({'Item': selected_item, 'Qty': qty, 'Rate': rate, 'Amount': amount, 'Profit': profit}, ignore_index=True)
            st.success(f"Added {selected_item} to invoice.")

    st.write("Invoice")
    st.dataframe(sales)

    total_amount = sales['Amount'].sum()
    st.write(f"Total Amount: {total_amount}")

    if st.button("Generate Bill"):
        pdf_file = generate_pdf_bill(sales, total_amount)
        st.success("Bill generated successfully!")
        st.download_button("Download Invoice", data=open(pdf_file, "rb"), file_name="invoice.pdf", mime="application/pdf")
