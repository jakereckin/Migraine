import streamlit as st
import datetime as dt
import sys
import time
import sys
import os
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



def get_client():
    uri = f"mongodb+srv://nda-admin:{st.secrets.get('mongo')['DB_PASSWORD']}@cluster0.jd3nwb7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)

def get_my_db(client):
    my_db = client['HEALTH']
    migraine = my_db['MIGRAINE_DATA']
    current_data = pd.DataFrame(list(migraine.find()))
    return migraine, current_data

def update_db(migraine,
              my_df,
              current_data):
    if len(current_data) > 0:
        my_df_test = pd.merge(current_data.drop(columns=['VALUE']),
                            my_df,
                            on=['_id',
                                'DATE',
                                'DATA_LABEL'],
                                how='outer',
                                indicator='exists')
        my_df = my_df_test[my_df_test['exists']=='right_only'].drop(columns=['exists'])
    if len(my_df) > 0:
        data_list = my_df.to_dict('records')
        migraine.insert_many(data_list, bypass_document_validation=True)
    return None

client = get_client()
migrane, current_data = get_my_db(client)
entry_types = ['Add Alcohol',
               'Add Morning Meditation',
               'Add Evening Meditation',
               'Add Traveling',
               'Add Pushups',
               'Add Planks',
               'Add Morning Happiness',
               'Add Night Happiness',
               'Add Magneisum',
               'Add Tylenol',
               'Add Migraine']
date = st.date_input(label='Enter Date')
if date:
    choice = st.selectbox(label='Choose Event',
                          options=entry_types)
    if choice == 'Add Alcohol':
        value = st.number_input(label='Drink Count', step=1)
        submit = st.button(label='Submit')
    elif choice in ['Add Morning Meditation',
                    'Add Evening Meditation',
                    'Add Planks']:
        value = st.number_input(label='Minutes', step=1)
        submit = st.button(label='Submit')
    elif choice in ['Add Morning Happiness',
                    'Add Night Happiness']:
        value = st.number_input(label='Happiness Level',
                                min_value=0,
                                max_value=10,
                                step=1)
        submit = st.button(label='Submit')
    elif choice in ['Add Traveling',
                    'Add Magneisum',
                    'Add Tylenol',
                    'Add Migraine']:
        value = st.radio(label='Flag', options=['Y', 'N'])
        submit = st.button(label='Submit')
    elif choice == 'Add Pushups':
        value = st.number_input(label='Count', step=5)
        submit = st.button(label='Submit')

    if submit:
        my_frame = pd.DataFrame([[date, choice, value]],
                         columns=['DATE', 'DATA_LABEL', 'VALUE']
        )
        my_frame['DATE'] = pd.to_datetime(my_frame['DATE']).dt.strftime('%m/%d/%Y')
        my_frame['_id'] = (my_frame['DATE']
                        + '_'
                        + my_frame['DATA_LABEL']
        )
        update_db(migraine=migrane,
                  my_df=my_frame,
                  current_data=current_data)
        time.sleep(.5)
        st.write(f'Added {choice} to DB for {date}')
#get_client()