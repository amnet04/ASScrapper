import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))

from ASScrapper import Scrapper
import random
import csv


url = "https://free-proxy-list.net/"
prv =  Scrapper("free-proxy-list",url, headless=True, str_folder="../examples", str_file="free-proxy-list-dot_net.csv")
prv.open_dom()
prv.configure_driver()
prv.driver.get(url)
prv.get_elements()

prv.get_navigate("../scrapped/free-proxy-list.csv")
prv.driver.close()

proxy_list = []
with open("../scrapped/free-proxy-list.csv", "r") as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		proxy_list.append(row['first_name'], row['last_name'])

print (proxy_list)