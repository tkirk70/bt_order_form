import streamlit as st
import pandas as pd
import base64
import datetime

now = datetime.datetime.now()
formatted_time = now.strftime("%Y%m%d%H%M%S")
# print(formatted_time)


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
st.header('Choose Style (SKU), Color and Size by selecting from list or typing')

col1, col2, col3, col4 = st.columns(4)

with col1:
    style = st.selectbox("Style", df_items['STYLE'].unique(), placeholder="Select a style...", index=None)
    
with col2:
    color = st.selectbox("Color", df_items['COLOR'].unique(), placeholder="Select a color...", index=None)
    
with col3:
    size = st.selectbox("Size", df_items['SIZE'].unique(), placeholder="Select a size...", index=None)
    
with col4:
    qty = st.number_input("Quantity", 1)
    
col5, col6, col7, col8, col9 = st.columns(5)

with col5:
    ht = st.selectbox('Hang Tags', (False, True))
    
with col6:
    cb = st.selectbox('Co-Branding', (False, True))
    
with col7:
    fl = st.selectbox('Folding', ('Printer', 'Retail'))
    
with col8:
    nl = st.selectbox('Neck Labels', (False, True))
    
with col9:
    st.selectbox('UPC Required', (False, True))
 
notes = st.text_input('Notes', value='')   
    
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
filtered_df['HangTags'] = ht
filtered_df['CoBrand'] = cb
filtered_df['Folding'] = fl
filtered_df['NeckLabels'] = nl
filtered_df['Notes'] = notes

st.dataframe(filtered_df, hide_index=True, width=1300)
df_concat = pd.concat([selected_row, filtered_df], axis=1, join='outer', ignore_index=True)
df_new = pd.DataFrame(columns=filtered_df.columns)
    
# shopping cart
st.header('Current Line Item')
st.dataframe(selected_row, hide_index=True, width=1300)
st.dataframe(filtered_df, hide_index=True, width=1300)
    
@st.cache(allow_output_mutation=True)
def get_data():
    return []

if st.button("Add Line Item"):
    get_data().append({'STYLE' : style, 'COLOR': color, 'SIZE' : size, 'DESCRIPT' : descript[0], 'UPC' : upc[0],
                       'QTY' : qty, 'TOTAL' : total1[0], 'HangTags' : ht, 'CoBrand' : cb, 'Folding' :fl, 'NeckLabels' : nl, 'Notes' : notes})
    
if st.button('Clear Order'):
    # Clear the input box after hitting enter
    get_data().clear()

st.header('Current Order')

st.write(pd.DataFrame(get_data()))
submit_df = pd.DataFrame(get_data())
# concatenate dataframes along the columns
result = pd.concat([selected_row, submit_df], axis=1, join='outer')

if st.button('Submit Order'):
    # Create a downloadable link for the DataFrame as a csv file
    csv = result.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="order_details_{formatted_time}.csv">Download Order Form</a>'
    st.markdown(href, unsafe_allow_html=True)
    # Write code to convert df to downloadable excel file.
    
    
##################################################################

'''

Adding send gmail section

'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config import *


password = st.text_input("Type your password and press enter:")
if st.button('Send Email'):
    

    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg['Cc'] = cc
    # msg['Body'] = 'Hello, did this work?'
    
    # # Attach the CSV file
    # attachment_path = f'order_details_{formatted_time}.csv'
    # attachment = open(attachment_path, 'rb')
    # part = MIMEBase('application', 'octet-stream')
    # part.set_payload(attachment.read())
    # encoders.encode_base64(part)
    # part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
    # msg.attach(part)
    
    # Send the email
    smtp_server = smtp_server
    smtp_port = smtp_port
    sender_email = sender
    sender_password = password
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        server.quit()
    
    st.write('Email sent successfully!')


