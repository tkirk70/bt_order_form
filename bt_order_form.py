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

# order input dropdowns

col1, col2, col3 = st.columns(3)

with col1:
    style = st.text_input("Style", 'KBT7011')
    
with col2:
    color = st.text_input("Color", 'NONE')
    
with col3:
    size = st.text_input("Size", 'ONESIZE')
    