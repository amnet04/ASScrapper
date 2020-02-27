import random
import csv
from tempfile import NamedTemporaryFile
import shutil

from ..utilities.dom import dom
from ..scrapper.ASScrapper import Scrapper

import pathlib
thispath=pathlib.Path(__file__).parent.parent.absolute()

FILE = "{}/{}".format(thispath,"scrapped/free-proxy-list.csv")

class scrappedProxyList():

	def __init__(self, url,strc_file, data_file, headless=True, max_next=0):
		print("\n ************************** Obteniendo listado de proxies ************* \n")
		
		dom_strc = dom(strc_file, ["Ip", "Port", "Country", "Anonymity"])
		self.data_str = dom_strc.data_str
		self.url = url
		self.strc_file = strc_file
		self.data_file = data_file
		self.headless = headless
		self.max_next = max_next
		del dom_strc

		self.scrapProxyLits()
		self.list = self.getUtilProxies()
		print("\n ************************** Listado de proxies obtenido *************** \n")
		

	def scrapProxyLits(self):
		print("************************** Scrapeando proxys")
		self.proxy_scrapper = Scrapper("free-proxy-list",
										self.url, 
					 					headless=self.headless, 
					 					str_folder="{}/{}".format(thispath,"examples"), 
					 					str_file="proxynova.csv")
		print("Recordar que str_file esta quemado")
		try:
			with open(self.data_file, "w") as w:
				w.write("Ip\tPort\tHttps\tCountry\tAnonymity\tFunctionality\n")

		except IOError as e:
			raise(e)

		self.proxy_scrapper.open_dom()
		self.proxy_scrapper.configure_driver()
		self.proxy_scrapper.driver.get(self.url)
		self.proxy_scrapper.get_elements()

		self.proxy_scrapper.get_navigate(self.data_file, 
						limit = 1, 
						insedesep=False)
		
		self.proxy_scrapper.driver.close()
		print("**************************  Fin del scrap de proxys")
		self.proxy_scrapper.driver.quit()


	def getUtilProxies(self):
		print("************************** Obteniendo proxys váldos")
		fields = ['Ip', 'Port', 'Https', 'Country', 'Anonymity', 'Functionality']
		with open("/home/sarnahorn/Programacion/Doctorado/asscrapper/scrapped/free-proxy-list.csv", 'r') as csvfile:
			reader = csv.DictReader(csvfile, delimiter="\t")
			ProxiList = [dict(a) for a in reader]
			utilProxiList = list(filter(lambda x : x["Functionality"] not in ["TimeOut","SomethingGoesWrong"], ProxiList))
			return utilProxiList
		print("************************** Proxies válidos obtenido")

	def modificateFunctionality(self, proxy, functionality):
		print("************************** Modificando estado del proxy: {}".format(proxy["Ip"]))
		tempfile = NamedTemporaryFile(mode='w', delete=False)

		fields = ['Ip', 'Port', 'Https', 'Country', 'Anonymity', 'Functionality']

		with open("/home/sarnahorn/Programacion/Doctorado/asscrapper/scrapped/free-proxy-list.csv", 'r') as csvfile, tempfile:
			reader = csv.DictReader(csvfile, fieldnames=fields, delimiter="\t")
			writer = csv.DictWriter(tempfile, fieldnames=fields, delimiter="\t")
			for row in reader:
				#print([row['Ip'], row['Port']], [Ip, '{}'.format(Port)], [row['Ip'], row['Port']] == [Ip, '{}'.format(Port)])
				if [row['Ip'], row['Port']] == [proxy["Ip"], proxy["Port"]]:
					print("Cachada")
					row['Functionality'] = functionality
				writer.writerow(row)

		shutil.move(tempfile.name, "/home/sarnahorn/Programacion/Doctorado/asscrapper/scrapped/free-proxy-list.csv")
		print("************************** Estado del proxy: {} modificado ".format(proxy["Ip"]))
