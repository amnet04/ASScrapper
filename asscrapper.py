import csv
from time import sleep
import threading
import timeit
from os import path, makedirs
from shutil import get_terminal_size
import datetime
import random
import validators.url
from os.path import isfile
import errno
import random

# Selenium
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import Firefox
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType


# Siblings
from asscrapper.utilities.dom import dom
from asscrapper.utilities.proxygetter import proxies
from asscrapper import logger

import pathlib
thispath=pathlib.Path(__file__).parent.parent.absolute()



class Scrapper():

	UserAgentList = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0",
					 "Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0",
					 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
					 "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0",
					 "Mozilla/5.0 (Windows NT 10.0; rv:68.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
					]

	def __init__(self, 
				 name, 
				 urls,
				 str_file,
				 test_url = "http://ipv4.plain-text-ip.com/",
				 #test_url = "https://www.york.ac.uk/teaching/cws/wws/webpage1.html", 
				 data_folder = "{}/scrapped".format(thispath),
				 proxy = False,
				 headless= False, 
				 wait=1,
				 max_nexts=0):

		logger.info("")
		logger.info("********************************************************************")
		logger.info("***               Inicializando el scrapper                      ***")
		logger.info("********************************************************************")
		logger.info("")

		self.name = name
		self.urls =  urls
		self.str_file = str_file
		self.test_url = test_url
		self.data_folder = "{}/{}".format(data_folder,self.name)
		
		self.proxy = proxy
		if self.proxy:
			self.actual_proxy = False
			if isinstance(self.proxy,dict):
				try: 
					self.proxy_list = proxies(typ=self.proxy["Types"], 
											  lim=self.proxy["Limit"], 
											  countries_list=self.proxy["Countries"])
				except:
					raise 
			else:
				self.proxy_list = proxies()
		else:
			self.proxy_list = False

		self.headless = headless
		self.wait = wait
		self.max_nexts = max_nexts
		
		

		self.data = []
		self.previus_data = []

		self.tread = False

		self.set_dom()
		self.configure_driver()
		self.crawl()

		
	def set_dom(self):
		dom_strc = dom(self.str_file)
		self.main_strc = dom_strc.main_strc
		self.data_strc = dom_strc.data_strc


	def configure_driver(self):
		self.firefox_capabilities = DesiredCapabilities.FIREFOX

		UserAgent = random.choice(self.UserAgentList)
		logger.info("User agent: {}".format(UserAgent))


		if self.headless:
			self.options = Options()
			self.options.add_argument('--headless')
			self.firefox_profile = FirefoxProfile()
			self.firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
			self.firefox_profile.set_preference("general.useragent.override", UserAgent)
			self.firefox_profile.update_preferences()
					
		else:
			self.options = Options()
			self.firefox_profile = FirefoxProfile()
			self.firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
			# Esta lineas no sirven por ahora, buscar alternativas
			"""self.firefox_profile.set_preference('permissions.default.image',2) 
			self.firefox_profile.set_preference("permissions.default.stylesheet",2)"""
			self.firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
			self.firefox_profile.set_preference('media.navigator.video.enabled',False)
			self.firefox_profile.set_preference('media.encoder.webm.enabled',False)
			self.firefox_profile.set_preference('media.ffmpeg.enabled',False)
			self.firefox_profile.set_preference('media.flac.enabled',False)
			self.firefox_profile.set_preference("general.useragent.override", UserAgent)
			self.firefox_profile.update_preferences()

		try:
			self.driver = Firefox(capabilities=self.firefox_capabilities, 
								  options=self.options, 
								  firefox_profile=self.firefox_profile, 
								  executable_path='geckodriver')
		except:
			raise



	def createDataFile(self):
		try:
			if not path.isdir(self.data_folder):
				makedirs(self.data_folder)
			if not path.isfile(self.data_file):
				with open(self.data_file, "w") as datafile:
					writer = csv.DictWriter(datafile, delimiter="\t", fieldnames=list(self.data_strc.keys()))
					writer.writeheader()
		except:
			raise

	
	def crawl(self):
		logger.info("Starting crawler")
		try:
			for enum, url in enumerate(self.urls):
				logger.info("Crawling {}".format(url["URL"]))
				filename = url["PARAM"].replace(" ","")
				self.data_file = "{}/{}.csv".format(self.data_folder,filename)
				self.createDataFile()
				self.url = url
				self.navigate()
			self.driver.close()
			logger.info("Finishing crawler")
		except:
			raise

	def navigate(self):
		try:
			self.set_proxy()
			self.driver.get(self.url["URL"])
			self.check_containers()
			self.get_data()
			self.nexts = 0
			self.next()
		except:
			self.navigate()

	def check_containers(self):
		try:
			print("---> Check containers")
			WebDriverWait(self.driver, 30).until(expected.visibility_of_element_located((By.CSS_SELECTOR, '{}'.format(self.main_strc["LiCont"]["Selector"]))))
			self.main_strc["LiCont"]["Elements"] = self.driver.find_elements_by_css_selector('{}'.format(self.main_strc["LiCont"]["Selector"]))
			self.main_strc["ElCont"]["Elements"] = []
		
			if self.main_strc["LiCont"]["Elements"] != []:
				for element in self.main_strc["LiCont"]["Elements"]:
					self.main_strc["ElCont"]["Elements"] += element.find_elements_by_css_selector('{}'.format(self.main_strc["ElCont"]["Selector"]))

			if self.actual_proxy:
				self.proxy_list.proxy_notwork(self.actual_proxy.ip, self.actual_proxy.port)
		
		except TimeoutException as e:
			print("---> Nos cacharon")

			if self.actual_proxy:
				self.proxy_list.proxy_notwork(self.actual_proxy.host, self.actual_proxy.port)
				self.set_proxy()
			try:
				self.driver.close()
				self.navigate(self)
			except:
				self.navigate(self)
				pass

			
		
		except WebDriverException as e:
			print("---> Ni idea que pasó")
			if self.actual_proxy:
				self.proxy_list.proxy_notwork(self.actual_proxy.ip, self.actual_proxy.port)
				verified_proxy_host = ""
				self.set_proxy()
			try:
				self.driver.close()
				self.navigate(self)
			except:
				self.navigate(self)
				pass									

	def get_data(self):
		try:
			if self.main_strc["ElCont"]["Elements"] != []:   
				for element in self.main_strc["ElCont"]["Elements"]:
					data_dict = {}
					for key, selector in self.data_strc.items(): 
						elements = element.find_elements_by_css_selector('{}'.format(selector["Selector"]))
						data_dict[key] = ""
						if key == "Link":
							data_dict[key] += elements[0].get_attribute('href')
						else:
							if len(elements) > 1:
								for e in elements:
									data_dict[key] += "<e>"+e.text+"</e>"
							elif len(elements)==1:
								data_dict[key] = elements[0].text
						
							
					with open(self.data_file, "a") as datafile:
						if "".join(list(data_dict.values())) != "":
							writer = csv.DictWriter(datafile, delimiter="\t", fieldnames=list(self.data_strc.keys()))
							writer.writerow(data_dict)
		except:
			raise

	def next(self):
		
		if self.main_strc["Next"]["Selector"]:
			self.nexts += 1
			#print(self.max_nexts, self.nexts, self.max_nexts == 0 or  self.nexts < self.max_nexts)
			if  self.max_nexts == 0 or  self.nexts < self.max_nexts:
				try:
					self.main_strc["Next"]["Elements"] = WebDriverWait(self.driver,2).until(expected.element_to_be_clickable((By.CSS_SELECTOR, '{}'.format(self.main_strc["Next"]["Selector"]))))
					wait = random.randrange(5,10)
					sleep(wait)
					self.main_strc["Next"]["Elements"].click()
					self.check_containers()
					self.get_data()
					self.next()
				except:
					raise

	def set_proxy(self):
		if self.proxy_list:

			self.proxy_list.select_proxy()
			self.actual_proxy = self.proxy_list.selected_proxy
			logger.info("Setting {}:{} from {} as proxy".format(self.actual_proxy.host, 
																self.actual_proxy.port, 
																self.actual_proxy.geo))

			self.driver.execute("SET_CONTEXT", {"context": "chrome"})

			try:
				self.driver.execute_script("""
					Services.prefs.setIntPref('network.proxy.type', 1);
					Services.prefs.setCharPref("network.proxy.http", arguments[0]);
					Services.prefs.setIntPref("network.proxy.http_port", arguments[1]);
					Services.prefs.setCharPref("network.proxy.ssl", arguments[0]);
					Services.prefs.setIntPref("network.proxy.ssl_port", arguments[1]);""",
					self.actual_proxy.host,self.actual_proxy.port
					)
				
			finally:
				self.driver.execute("SET_CONTEXT", {"context": "content"})
				self.test_proxy()

		else:
			logger.info("------------------------La cagó pedazo e bola!!!!")

		"""
		Services.prefs.setIntPref('network.proxy.type', 1);
		Services.prefs.setCharPref("network.proxy.http", arguments[0]);
		Services.prefs.setIntPref("network.proxy.http_port", arguments[1]);
		Services.prefs.setCharPref("network.proxy.ssl", arguments[0]);
		Services.prefs.setIntPref("network.proxy.ssl_port", arguments[1]);
		Services.prefs.setCharPref("network.proxy.ftp", arguments[0]);
		Services.prefs.setIntPref("network.proxy.ftp_port", arguments[1]);
		"""
				
			
	def test_proxy(self, timeout = 10):
		if self.actual_proxy:
			logger.info("Testing {}:{} from {} as proxy".format(self.actual_proxy.host))
			try:
				self.driver.set_page_load_timeout(timeout)
				self.driver.get(self.test_url)
				logger.info("{} worked in test page".format(self.actual_proxy.host))

			except TimeoutException as e:
				if timeout == 10:
					test_proxy(self, timeout = 20)
				else:
					logger.info("{} Time out".format(self.actual_proxy.host))	
					self.proxy_list.proxy_notwork(self.actual_proxy.host self.actual_proxy.port)
					self.set_proxy()

			except WebDriverException as e:				
				logger.info("{} Something goes wrong".format(self.actual_proxy.host))
				self.proxy_list.proxy_notwork(self.actual_proxy.ip, self.actual_proxy.port)
				self.set_proxy()