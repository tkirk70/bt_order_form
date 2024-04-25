import streamlit as st
import pandas as pd
import base64

# set layout
st.set_page_config(page_title=None, page_icon=None, layout="wide")
# st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)



df_cust = pd.read_csv('Bourbon Trail Customer List.csv')
col_left, col_right = st.columns([3,1])
with col_left:
     st.title("Bourbon Trail Order Form")
with col_right:
    st.image('bt.jpg')

# Dropdown for product selection
selected_cust = st.selectbox("Select a customer", df_cust['Company'])

# Display product details
st.write(f"Selected Customer: **{selected_cust}**")

# Filter the DataFrame based on the selected customer
selected_row = df_cust[df_cust['Company'] == selected_cust]
# st.dataframe(selected_row, hide_index=True, width=1300)

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
upc = filtered_df['UPC'].values
descript = filtered_df['DESCRIPT'].values
total1 = filtered_df["Total"] = filtered_df["Total"].values
st.dataframe(filtered_df, hide_index=True, width=1300)
df_concat = pd.concat([selected_row, filtered_df], axis=1, join='outer', ignore_index=True)
df_new = pd.DataFrame(columns=filtered_df.columns)
    
# shopping cart
st.header('Current Order')
st.dataframe(selected_row, hide_index=True, width=1300)
st.dataframe(filtered_df, hide_index=True, width=1300)
    
@st.cache(allow_output_mutation=True)
def get_data():
    return []

if st.button("Add Line Item"):
    get_data().append({'STYLE' : style, 'COLOR': color, 'SIZE' : size, 'DESCRIPT' : descript, 'UPC' : upc,
                       'QTY' : qty, 'TOTAL' : total1})
    
if st.button('Clear Order'):
    # Clear the input box after hitting enter
    get_data().clear()

st.write(pd.DataFrame(get_data()))
submit_df = pd.DataFrame(get_data())
# concatenate dataframes along the columns
result = pd.concat([selected_row, submit_df], axis=1, join='outer')

if st.button('Submit Order'):
    # Create a downloadable link for the DataFrame as an Excel file
    csv = result.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="order_details.csv">Download Order Form</a>'
    st.markdown(href, unsafe_allow_html=True)
    # Write code to convert df to downloadable excel file.