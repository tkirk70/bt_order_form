import streamlit as st
import pandas as pd

df_cust = pd.read_csv('Bourbon Trail Customer List.csv')

st.title("Bourbon Trail Order Form")

# Dropdown for product selection
selected_cust = st.selectbox("Select a customer", df_cust['Company'])

# Display product details
st.write(f"Selected Customer: **{selected_cust}**")

# Filter the DataFrame based on the selected customer
selected_row = df_cust[df_cust['Company'] == selected_cust]
st.dataframe(selected_row, hide_index=True)

# read the items database
df_items = pd.read_excel('KBTPriceList 4.27.22.xlsx', sheet_name='Datasheet')

# order input dropdowns

col1, col2, col3, col4 = st.columns(4)

with col1:
    style = st.selectbox("Style", df_items['STYLE'].unique())
    
with col2:
    color = st.selectbox("Color", df_items['COLOR'].unique())
    
with col3:
    size = st.selectbox("Size", df_items['SIZE'].unique())
    
with col4:
    size = st.number_input("Quantity", 1)
    
# get upc from the values above
# Filter the DataFrame based on the selected values
filtered_df = df_items[df_items['STYLE'] == style]

st.dataframe(filtered_df, hide_index=True)
    