import streamlit as st
import datetime as dt
import sys
import time
import sys
import os
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

@st.cache_resource
def get_client():
    uri =  f"mongodb+srv://nda-admin:{st.secrets['mongo']['MONGODB_PASSWORD']}@cluster0.jd3nwb7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client

def get_my_dbs(client):
    my_db = client['HEALTH']
    garmin = my_db['GARMIN_DATA']
    migraine = my_db['MIGRAINE_DATA']
    return garmin, migraine

def to_pandas_frame(garmin, migraine):
    garmin_df = pd.DataFrame(list(garmin.find())).drop(columns=['_id'])
    migraine_df = pd.DataFrame(list(migraine.find())).drop(columns=['_id'])
    full_frame = (pd.concat([garmin_df,
                             migraine_df])
                    .reset_index(drop=True))
    return full_frame

password_box = st.text_input(label='Enter Password', 
                             type='password')
if password_box == st.secrets['mongo']['PAGE_PASSWORD']:
    client = get_client()
    garmin, migraine = get_my_dbs(client)
    full_frame = to_pandas_frame(garmin=garmin,
                                migraine=migraine)

    st.dataframe(full_frame,
                 use_container_width=True,
                 hide_index=True
    )