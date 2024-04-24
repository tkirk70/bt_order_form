import streamlit as st
import pandas as pd

df_cust = pd.read_csv('Bourbon Trail Customer List.csv')
df_cust

st.title("Bourbon Trail Order Form")

# Dropdown for product selection
selected_cust = st.selectbox("Select a customer", df_cust['Company'])

# Display product details
st.write(f"Selected Customer: **{selected_cust}**")
st.write(f"{df_cust[df_cust['Company']]} == {selected_cust}")