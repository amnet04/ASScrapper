import random
import csv
from tempfile import NamedTemporaryFile
import shutil
from time import sleep

from ..utilities.dom import dom
from asscrapper import logger
from asscrapper import asscrapper as assc

import pathlib
thispath=pathlib.Path(__file__).parent.parent.absolute()

FILE = "{}/{}".format(thispath,"proxies")

class scrappedProxyList():

	def __init__(self, url,strc_file, data_folder, headless=True, max_nexts=1):
		logger.info("Getting the list of proxies from: {}".format(url[0]["URL"]))
		dom_strc = dom(strc_file, ["Ip", "Port", "Country", "Anonymity"])
		self.data_strc = dom_strc.data_strc
		self.url = url
		self.strc_file = strc_file
		self.data_folder = data_folder
		self.headless = headless
		self.max_nexts = max_nexts
		self.fields = ["Ip", "Port", "Country", "Anonymity", "Functionality"]
		self.file = "{}/proxies/{}.csv".format(self.data_folder,self.url[0]["PARAM"])

		self.scrapProxyLits()
		self.list = self.getUtilProxies()
		logger.info("{} proxies found".format(len(self.list)))
		
		
	def scrapProxyLits(self):
		try:
			with open(self.file, "w") as f:
				f.write("\t".join(self.fields)+"\n")
		except:
			raise
		prv = assc.Scrapper("proxies", 
                   self.url, 
                   self.strc_file,
                   proxy = False,
                   data_folder = self.data_folder,
                   headless = self.headless,
                   max_nexts = self.max_nexts)


	def getUtilProxies(self):
		with open(self.file, 'r') as csvfile:
			reader = csv.DictReader(csvfile, delimiter="\t")
			ProxyList = [dict(a) for a in reader]
			if len(ProxyList) < 1:
				sleep(1)
				self.getUtilProxies()
		utilProxyList = list(filter(lambda x : x["Functionality"] in ["Worked", "", None], ProxyList))
		logger.info("{} util proxies found of {}".format(len(utilProxyList), len(ProxyList)))
		return utilProxyList

	def modificateFunctionality(self, proxy, functionality):
		tempfile = NamedTemporaryFile(mode='w', delete=False)
		self.getUtilProxies()
		with open(self.file, 'r') as csvfile, tempfile:
			reader = csv.DictReader(csvfile, delimiter="\t")
			writer = csv.DictWriter(tempfile, fieldnames=self.fields, delimiter="\t")
			writer.writeheader()
			for row in reader:
				if [row['Ip'], row['Port']] == [proxy["Ip"], proxy["Port"]]:
					logger.info("Changing functionality of {} to {}".format(row['Ip'], functionality))
					row['Functionality'] = functionality
				writer.writerow(row)
		shutil.move(tempfile.name, self.file)

