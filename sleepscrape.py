import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json
from pprint import pprint
import csv
from time import sleep


APIKEY = "24ac0c9369d539a9c2cdb7aa8bac2bd4dfaf022c"
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
# def main():


 # run forever...
while True:
    try:
        r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME})
        print("ok")
        print(r.url)
        print(r.status_code)
        # store(json.loads(r.text))

        time.sleep(5)
    except:
    # if there is any problem, print the traceback
        print("traceback")
#  return
