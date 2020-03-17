import random
import csv
from tempfile import NamedTemporaryFile
import shutil

from ..utilities.dom import dom
from ..scrapper import asscrapper

import pathlib
thispath=pathlib.Path(__file__).parent.parent.absolute()

FILE = "{}/{}".format(thispath,"proxies")

class scrappedProxyList():

	def __init__(self, url,strc_file, data_folder, headless=True, max_nexts=1):
		print("\n ************************** Obteniendo listado de proxies ************* \n")
		dom_strc = dom(strc_file, ["Ip", "Port", "Country", "Anonymity"])
		self.data_strc = dom_strc.data_strc
		self.url = url
		self.strc_file = strc_file
		self.data_folder = data_folder
		self.headless = headless
		self.max_nexts = max_nexts
		self.fields = ["Ip", "Port", "Country", "Anonymity", "Functionality"]

		self.scrapProxyLits()
		self.list = self.getUtilProxies()
		print("\n ************************** Listado de proxies obtenido *************** \n")
		

	def scrapProxyLits(self):
		print("************************** Scrapeando proxys")
		prv = asscrapper.Scrapper("proxies", 
                   self.url, 
                   self.strc_file,
                   proxy = False,
                   data_folder = self.data_folder,
                   headless = self.headless,
                   max_nexts = self.max_nexts)

		self.file = "{}/{}.csv".format(prv.data_folder,self.url[0]["PARAM"])

		tempfile = NamedTemporaryFile(mode='w', delete=False)
		with open(self.file, 'r') as csvfile, tempfile:
			reader = csv.DictReader(csvfile, fieldnames=self.fields, delimiter="\t")
			writer = csv.DictWriter(tempfile, fieldnames=self.fields, delimiter="\t")
			for row in reader:
				row['Functionality'] = "Not_Tested"
				writer.writerow(row)
		shutil.move(tempfile.name, self.file)


		print("**************************  Fin del scrap de proxys")


	def getUtilProxies(self):
		print("************************** Obteniendo proxys váldos")
		with open(self.file, 'r') as csvfile:
			reader = csv.DictReader(csvfile, fieldnames=self.fields, delimiter="\t")
			ProxiList = [dict(a) for a in reader]
			utilProxiList = list(filter(lambda x : x["Functionality"] not in ["TimeOut","SomethingGoesWrong"], ProxiList))
			return utilProxiList
		print("************************** Proxies válidos obtenidos")

	def modificateFunctionality(self, proxy, functionality):
		print("************************** Modificando estado del proxy: {}".format(proxy["Ip"]))
		tempfile = NamedTemporaryFile(mode='w', delete=False)

		with open(self.file, 'r') as csvfile, tempfile:
			reader = csv.DictReader(csvfile, fieldnames=self.fields, delimiter="\t")
			writer = csv.DictWriter(tempfile, fieldnames=self.fields, delimiter="\t")
			for row in reader:
				#print([row['Ip'], row['Port']], [Ip, '{}'.format(Port)], [row['Ip'], row['Port']] == [Ip, '{}'.format(Port)])
				if [row['Ip'], row['Port']] == [proxy["Ip"], proxy["Port"]]:
					print("Cachada")
					row['Functionality'] = functionality
				writer.writerow(row)

		shutil.move(tempfile.name, self.file)
		print("************************** Estado del proxy: {} modificado ".format(proxy["Ip"]))
