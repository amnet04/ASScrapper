import random
import csv
from ..scrapper.ASScrapper import Scrapper

import pathlib
thispath=pathlib.Path(__file__).parent.parent.absolute()

def proxyRotator():

	url = "https://free-proxy-list.net/"
	proxy_scrapper =  Scrapper("free-proxy-list",
					 url, 
					 headless=True, 
					 str_folder="{}/{}".format(thispath,"examples"), 
					 str_file="free-proxy-list-dot_net.csv")

	filename = "{}/{}".format(thispath,"scrapped/free-proxy-list.csv")
	
	try:
		with open(filename, "w") as w:
			w.write("Ip\tPort\tHttps\n")

	except IOError as e:
		raise(e)


	proxy_scrapper.open_dom()
	proxy_scrapper.configure_driver()
	proxy_scrapper.driver.get(url)
	proxy_scrapper.get_elements()

	proxy_scrapper.get_navigate("{}/{}".format(thispath,"scrapped/free-proxy-list.csv"), 
					limit = 3, 
					insedesep=False)
	proxy_scrapper.driver.close()

	with open(filename, "r") as csvfile:
		proxys= csv.DictReader(csvfile, delimiter="\t")
		proxy_list = [dict(x) for x in list(proxys)]

	return proxy_list

