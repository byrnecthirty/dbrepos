import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import sqlalchemy as sqla
from sqlalchemy import create_engine
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
import datetime
import time
import mysql.connector

headers = {
    "Accept": "application/json"
}

APIKEY = "24ac0c9369d539a9c2cdb7aa8bac2bd4dfaf022c"
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

URI = "dublinbikes.cts6ewdbpn6n.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "dublinbikes"
USER = "dublinbikes"
PASSWORD = "PuRple55"

# r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME}, headers = headers)
# print(r.url)
# print(r.status_code)
# # pprint(json.loads(r.text))


# a = requests.get("{}/{}".format(STATIONS_URI, 42),
# params={"apiKey": APIKEY, "contract": NAME})
# pprint(json.loads(a.text))


engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER,PASSWORD,URI,PORT,DB), echo=True)
connection = engine.connect()



# stream_df = pd.DataFrame(columns=( 'address' , 'available_bike_stands' , 'available_bikes' , 'banking' , 'bike_stands' , 'bonus', 'contract_name' , 'last_update' , 'name' , 'number' , 'position' , 'status' ))


# stream_df.to_sql(name='streams', con=engine, if_exists = 'append', index=False)

# sql = "Select * from firsttable"

sqldatabase = "CREATE DATABASE IF NOT EXISTS dublinbikes"

connection.execute(sqldatabase)

sqltable = """ 
CREATE TABLE IF NOT EXISTS station ( 
address VARCHAR(256),
available_bike_stands INTEGER,
available_bikes INTEGER,
banking INTEGER,
bike_stands INTEGER,
bonus INTEGER,
contract_name VARCHAR(256),
last_update INTEGER, 
name VARCHAR(256), 
number INTEGER, 
position_lat REAL, 
position_lng REAL, 
status VARCHAR(256))"""

# connection.execute("INSERT into firsttable... .. . . .. . . ")
# stream_df.to_sql(name='streams', con=engine, if_exists = 'append', index=False)

try: 
    # res = connection.execute("DROP TABLE IF EXISTS station")
    res = connection.execute(sqltable)
    print(res.fetchall())
except Exception as e:
    print(e)

print("i made it")

# connection = engine.connect()
# result = connection.execute("select username from users")
# for row in r:
#     print("name:", row['name'])
# connection.close()


# data = r.json() 

# this works, writes to csvfile
# with open("guns.csv", "wb") as csvfile:
#     f = csv.writer(csvfile)
#     f.writerow(["address"]) # write the headers if you like
#     for elem in data:
#         f.writerow([])



# def write_to_file(text):
#     with open("data/bikes_{}".format(now.replace(" ", "_"), "w") as f:
#         f.write(r.text)

def stations_to_db(text):
    stations = json.loads(text)
    print("i am looking at the stations")
    for station in stations:
        print(type(station), len(station))
        vals=(station.get('address'), station.get('available_bike_stands'), station.get('available_bikes'), int(station.get('banking')), station.get('bike_stands'), int(station.get('bonus')), station.get('contract_name'), station.get('last_update'), station.get('name'), station.get('number'), station.get('position').get('lat'), station.get('position').get('lng'), station.get('status')
        )
        connection.execute("insert into station values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", vals)
        print(vals)
        print("i got to this point")
    return

def main():

    # run forever...
    # while True:
    try:
        response = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME})
        print("i have made my request")
        # print(r.url)
        # print(r.status_code)
        # print(json.loads(r.text))
        # store(json.loads(r.text))
        # now = datetime.datetime.now()
        # print(r,now)
        # a = requests.get("{}/{}".format(STATIONS_URI, 42),params={"apiKey": APIKEY, "contract": NAME})
        
        print('_____________')
        pprint(json.loads(response.text))

        # print(type(response.text))

        stations_to_db(response.text)

        # now sleep for 5 minutes
        time.sleep(20)
    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())
    return

if __name__ == "__main__":
    main()
# 
