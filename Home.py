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
    uri = st.write(f"mongodb+srv://nda-admin:{st.secrets.get('mongo')['DB_PASSWORD']}@cluster0.jd3nwb7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)

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

client = get_client()
st.write(st.secrets.get('mongo'))
garmin, migraine = get_my_dbs(client)
full_frame = to_pandas_frame(garmin=garmin,
                             migraine=migraine)

st.dataframe(full_frame)