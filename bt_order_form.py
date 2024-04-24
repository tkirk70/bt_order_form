import streamlit as st
import pandas as pd

# set layout
st.set_page_config(page_title=None, page_icon=None, layout="wide")
# st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)



df_cust = pd.read_csv('Bourbon Trail Customer List.csv')

st.title("Bourbon Trail Order Form")

# Dropdown for product selection
selected_cust = st.selectbox("Select a customer", df_cust['Company'])

# Display product details
st.write(f"Selected Customer: **{selected_cust}**")

# Filter the DataFrame based on the selected customer
selected_row = df_cust[df_cust['Company'] == selected_cust]
st.dataframe(selected_row, hide_index=True, width=1300)

# read the items database
df_items = pd.read_excel('KBTPriceList 4.27.22.xlsx', sheet_name='Datasheet', dtype={'UPC' : str})
# apply strip() method to all strings in DataFrame
df_items = df_items.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df_items = df_items.drop(['COLOR/SIZE/DESCRIPT'], axis=1)


# order input dropdowns
st.header('Current Line Item')

col1, col2, col3, col4 = st.columns(4)

with col1:
    style = st.selectbox("Style", df_items['STYLE'].unique(), placeholder="Select a style...", index=None)
    
with col2:
    color = st.selectbox("Color", df_items['COLOR'].unique(), placeholder="Select a color...", index=None)
    
with col3:
    size = st.selectbox("Size", df_items['SIZE'].unique(), placeholder="Select a size...", index=None)
    
with col4:
    qty = st.number_input("Quantity", 1)
    
# get upc from the values above
# Filter the DataFrame based on the selected values

filtered_df = df_items[
    (df_items['STYLE'] == style) &
    (df_items['COLOR'] == color) &
    (df_items['SIZE'] == size)
]
filtered_df['QTY'] = qty
total = qty * filtered_df['MSRP']
filtered_df["Total"] = total
filtered_df["Total"] = filtered_df["Total"].apply(lambda x: '${:,.2f}'.format(x))
st.dataframe(filtered_df, hide_index=True, width=1300)
df_concat = pd.concat([selected_row, filtered_df], axis=1, join='outer')
df_new = pd.DataFrame(columns=df_items.columns)


#adding a button

if st.button('Add to order'):

    st.write('Adding current choice and clearing dropdowns.') #displayed when the button is clicked
    df_new.append(filtered_df, ignore_index = True)
    

else:

    st.write('') #displayed when the button is unclicked
    
# shopping cart
st.header('Current Order')
st.dataframe(selected_row, hide_index=True, width=1300)
st.dataframe(filtered_df, hide_index=True, width=1300)


st.write('Concat axis=1 join=outer')
st.dataframe(df_concat, width=1300)
    
if st.button('Finish order'):

    st.write('Processing') #displayed when the button is clicked

else:

    st.write('') #displayed when the button is unclicked
    
st.write('df_new')
st.dataframe(df_new)

    