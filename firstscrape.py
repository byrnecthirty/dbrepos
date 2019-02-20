import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import sqlalchemy as sqla
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import json
from pprint import pprint
import csv
import pandas as pd
# import MySQLdb as mysqldb
import sqlalchemy as sqla
import traceback
import glob
import os
from pprint import pprint
# import simplejson as json
import requests
import time
import mysql.connector
from IPython.display import display

headers = {
    "Accept": "application/json"
}

APIKEY = "24ac0c9369d539a9c2cdb7aa8bac2bd4dfaf022c"
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

URI = "mydublinbikes.cts6ewdpn6n.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "mydublinbikes"
USER = "mydublinbikes"
PASSWORD = "PuRple55"

r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME}, headers = headers)
print(r.url)
print(r.status_code)
# pprint(json.loads(r.text))


a = requests.get("{}/{}".format(STATIONS_URI, 42),
params={"apiKey": APIKEY, "contract": NAME})
pprint(json.loads(a.text))
print("traceback")

stream_df = pd.DataFrame(columns=( 'address' , 'available_bike_stands' , 'available_bikes' , 'banking' , 'bike_stands' , 'bonus', 'contract_name' , 'last_update' , 'name' , 'number' , 'position' , 'status' ))

engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER,PASSWORD,URI,PORT,DB), echo=True)


# stream_df.to_sql(name='streams', con=engine, if_exists = 'append', index=False)

sql = """
CREATE DATABASE IF NOT EXISTS dbbikes;
"""
engine.execute(sql)
print("i made it")

# connection = engine.connect()
# # stream_df.to_sql(name='streams', con=engine, if_exists = 'append', index=False)
# result = connection.execute("select username from users")
# for row in r:
#     print("name:", row['name'])
# connection.close()


# data = r.json() 


# with open("guns.csv", "wb") as csvfile:
#     f = csv.writer(csvfile)
#     f.writerow(["address"]) # write the headers if you like
#     for elem in data:
#         f.writerow([])