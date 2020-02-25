import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))

from ASScrapper import Scrapper
import random
import csv


url = "https://free-proxy-list.net/"
prv =  Scrapper("free-proxy-list",url, headless=False, str_folder="../examples", str_file="free-proxy-list-dot_net.csv")
prv.open_dom()
prv.configure_driver()
prv.driver.get(url)
prv.get_elements()

prv.get_navigate("../scrapped/free-proxy-list.csv")
prv.driver.close()

