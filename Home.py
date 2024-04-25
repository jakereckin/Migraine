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
    uri = st.secrets["mongo"]["connection_string"]
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    st.write(client.admin.command('ping'))
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

client = get_client()
garmin, migraine = get_my_dbs(client)
full_frame = to_pandas_frame(garmin=garmin,
                             migraine=migraine)

st.dataframe(full_frame)