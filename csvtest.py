import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json
from pprint import pprint
import csv

APIKEY = "24ac0c9369d539a9c2cdb7aa8bac2bd4dfaf022c"
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"


r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME})
json_data = r.text

json_parsed = json.loads(json_data)

employ_data = open('buns.csv', 'w')

csvwriter = csv.writer(employ_data)

count = 0

for emp in json_parsed:

      if count == 0:

             header = emp.keys()

             csvwriter.writerow(header)

             count += 1

      csvwriter.writerow(emp.values())

employ_data.close()

# with open("buns.csv", "wb") as csvfile:
#     f = csv.writer(csvfile)
#     for elem in json_parsed:
#         f.writerow([json_parsed['name'][0], json_parsed['number'][0]])