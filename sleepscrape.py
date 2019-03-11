import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json
from pprint import pprint
import csv
import time
from time import sleep
import traceback


APIKEY = "24ac0c9369d539a9c2cdb7aa8bac2bd4dfaf022c"
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
# def main():


def main():

    # run forever...
    while True:
            try:
                r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME})
                print("ok")
                print(r.url)
                print(r.status_code)
                # print(json.loads(r.text))
                # store(json.loads(r.text))
                
                a = requests.get("{}/{}".format(STATIONS_URI, 42),params={"apiKey": APIKEY, "contract": NAME})
                pprint(json.loads(a.text))
                # now sleep for 5 minutes
                time.sleep(5)
            except:
                # if there is any problem, print the traceback
                print(traceback.format_exc())
    return


if __name__ == "__main__":
    main()


#  # run forever...
# while True:
#     try:
#         r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME})
#         print("ok")
#         print(r.url)
#         print(r.status_code)
#         # json.loads(r.text)

#         # time.sleep(5)
#     except:
#     # if there is any problem, print the traceback
#         print("traceback")
# #  return
