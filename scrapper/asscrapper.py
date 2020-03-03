import logging
import csv
from time import sleep
import timeit
from os import path, makedirs
from shutil import get_terminal_size
import datetime
import random
import validators.url
from os.path import isfile
import errno



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


"""logging.basicConfig(filename="scrapper.log",
					level=logging.DEBUG,
					format='%(asctime)s - %(message)s')"""

import pathlib
thispath=pathlib.Path(__file__).parent.parent.absolute()

# Siblings
from ..utilities.dom import dom
#from ..utilities.freeProxyRotator import scrappedProxyList

class Scrapper():

	def __init__(self, 
				 name, 
				 urls,
				 str_file,
				 test_url = "https://www.gelbukh.com/nlplinks.html", 
				 data_folder = "{}/scrapped".format(thispath),
				 proxy = False,
				 headless= False, 
				 wait=1,
				 max_nexts=0):

		self.name = name
		self.urls =  urls
		self.str_file = str_file
		self.test_url = test_url
		self.data_folder = "{}/{}".format(data_folder,self.name)
		self.proxy = proxy
		self.headless = headless
		self.wait = wait
		self.max_nexts = max_nexts

		self.data = []
		self.previus_data = []

		self.set_dom()
		self.set_proxylist()
		self.configure_driver()



		self.crawl()


	def set_proxylist(self):
		if self.proxy:
			try:
				self.proxy_list = scrappedProxyList(self.proxy["url"], self.proxy["str_file"], self.proxy["out_file"], headless=False)
			except ValueError as e:
				print (e)

	def set_dom(self):
		dom_strc = dom(self.str_file)
		print("----> ",dom_strc.data_strc)
		self.main_strc = dom_strc.main_strc
		self.data_strc = dom_strc.data_strc

	def configure_driver(self):
		self.firefox_capabilities = DesiredCapabilities.FIREFOX

		if self.headless:
			self.options = Options()
			self.options.add_argument('--headless')
			self.firefox_profile = FirefoxProfile()
			self.firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
					
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
			self.firefox_profile.update_preferences()

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
		print("\n")
		print(''.center(get_terminal_size()[0], '*'))
		print('---> Comenzando el crawling <--- '.center(get_terminal_size()[0], '*'))
		try:
			self.driver = Firefox(capabilities=self.firefox_capabilities, 
							  options=self.options, 
							  firefox_profile=self.firefox_profile, 
							  executable_path='geckodriver')
			#self.set_proxy()
			#self.test_proxy()
			start_time = timeit.default_timer()
			total_urls = len(self.urls)
			for enum, url in enumerate(self.urls):
				filename = url["PARAM"].replace(" ","")
				self.data_file = "{}/{}.csv".format(self.data_folder,filename)
				self.createDataFile()
				elapsed = float("{0:.2f}".format(timeit.default_timer() - start_time))
				percent = float("{0:.2f}".format(enum/total_urls))
				print('---> Url {} de {}, porcentaje {}\t {} segundos'.format(enum+1, total_urls, percent,elapsed),
					 end = "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r")
				self.url = url
				self.navigate()
			self.driver.close()
		except:
			raise
		print("---> Crawling finalizado <---".center(get_terminal_size()[0], '*'))
		print(''.center(get_terminal_size()[0], '*'))
		print("\n")

	def navigate(self):
		try:
			self.driver.get(self.url["URL"])
			self.check_containers()
			self.get_data()
			self.nexts = 0
			self.next()
		except:
			raise

	def check_containers(self):
		try:
			WebDriverWait(self.driver, 30).until(expected.visibility_of_element_located((By.CSS_SELECTOR, '{}'.format(self.main_strc["LiCont"]["Selector"]))))
			self.main_strc["LiCont"]["Elements"] = self.driver.find_elements_by_css_selector('{}'.format(self.main_strc["LiCont"]["Selector"]))
			self.main_strc["ElCont"]["Elements"] = []
		
			if self.main_strc["LiCont"]["Elements"] != []:
				for element in self.main_strc["LiCont"]["Elements"]:
					self.main_strc["ElCont"]["Elements"] += element.find_elements_by_css_selector('{}'.format(self.main_strc["ElCont"]["Selector"]))

		except:
			raise


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
				
			

			

		



	'''


		 

		
		del dom_strc
		
		self.data = []
		
		self.proxy = proxy
		self.actual_proxy = False
		self.proxy_list = False
		print(isfile(self.proxy["str_file"]))
		if validators.url(self.proxy["url"]) and isfile(self.proxy["str_file"]):
			self.proxy_list = scrappedProxyList(self.proxy["url"], self.proxy["str_file"], self.proxy["out_file"])
		else:
			print(":::::::::::::::: Working whitout proxy")

		self.headless = headless
		self.wait = wait
		self.max_next = 0
		self.time_out = 35
		self.data_auto_delimter = ("<e>","</e>")
		
		
		self.configure_driver()
		self.driver = Firefox(capabilities=self.firefox_capabilities, options=self.options, firefox_profile=self.firefox_profile, executable_path='geckodriver')
		self.set_proxy()
		self.test_proxy()
		for url in self.urls:
			self.url = url["URL"]
			self.out_file = "{}/{}.csv".format(self.datafolder, url["PARAM"])
			self.test_proxy()
			self.scrap()
		#self.driver.close()

	def configure_driver(self):
		print(">Configurando el driver -----------------------")

		self.firefox_capabilities = DesiredCapabilities.FIREFOX
					def configure_driver(self):
		print(">Configurando el driver -----------------------")

		self.firefox_capabilities = DesiredCapabilities.FIREFOX
				

		if self.proxy_list:
			if len(self.proxy_list.list) != 0:

				self.actual_proxy = self.proxy_list.getUtilProxies()[0]
				self.firefox_capabiliti> Configurando el dom <--- *********")
		self.filename = strc_file
		self.strc_fields = ["LiCont", "ElCont", "Next", "End", "Captcha"]
		self.data_fields = des['marionette'] = True

				self.firefox_capabilities['proxy'] = {
					"proxyType": "MANUAL",
					"httpProxy": "{}:{}".format(self.actual_proxy["Ip"],self.actual_proxy["Port"]),
					"sslProxy": "{}:{}".format(self.actual_proxy["Ip"],self.actual_proxy["Port"])
				}

		if self.headless:
			self.options = Options()
			self.options.add_argument('--headless')
			self.firefox_profile = FirefoxProfile()
			self.firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
					
		else:
			self.options = Options()
			self.firefox_profile = FirefoxProfile()
			self.firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
			self.firefox_profile.set_preference('permissions.default.image',2)
			self.firefox_profile.set_preference("permissions.default.stylesheet",2)
			self.firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
			self.firefox_profile.set_preference('media.navigator.video.enabled',False)
			self.firefox_profile.set_preference('media.encoder.webm.enabled',False)
			self.firefox_profile.set_preference('media.ffmpeg.enabled',False)
			self.firefox_profile.set_preference('media.flac.enabled',False)
			self.firefox_profile.update_preferences()

		print(">Driver configurado -----------------------")

		if self.proxy_list:
			if len(self.proxy_list.list) != 0:

				self.actual_proxy = self.proxy_list.getUtilProxies()[0]
				self.firefox_capabiliti> Configurando el dom <--- *********")
		self.filename = strc_file
		self.strc_fields = ["LiCont", "ElCont", "Next", "End", "Captcha"]
		self.data_fields = des['marionette'] = True

				self.firefox_capabilities['proxy'] = {
					"proxyType": "MANUAL",
					"httpProxy": "{}:{}".format(self.actual_proxy["Ip"],self.actual_proxy["Port"]),
					"sslProxy": "{}:{}".format(self.actual_proxy["Ip"],self.actual_proxy["Port"])
				}

		if self.headless:
			self.options = Options()
			self.options.add_argument('--headless')
			self.firefox_profile = FirefoxProfile()
			self.firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
					
		else:
			self.options = Options()
			self.firefox_profile = FirefoxProfile()
			self.firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
			self.firefox_profile.set_preference('permissions.default.image',2)
			self.firefox_profile.set_preference("permissions.default.stylesheet",2)
			self.firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
			self.firefox_profile.set_preference('media.navigator.video.enabled',False)
			self.firefox_profile.set_preference('media.encoder.webm.enabled',False)
			self.firefox_profile.set_preference('media.ffmpeg.enabled',False)
			self.firefox_profile.set_preference('media.flac.enabled',False)
			self.firefox_profile.update_preferences()

		print(">Driver configurado -----------------------")

	def test_proxy(self):
		if self.actual_proxy:
			print("!!!! > Testing {}".format(self.actual_proxy["Ip"]))
			try:
				self.driver.quit()
				self.driver.set_page_load_timeout(10)
				self.driver.get(self.test_url)
				self.proxy_list.modificateFunctionality(self.actual_proxy, "Worked")
			except TimeoutException as e:
				self.driver.quit()
				print("-- {} no fue capas de conectarse en 10 segundos".format(self.actual_proxy["Ip"]))	
				self.proxy_list.modificateFunctionality(self.actual_proxy, "TimeOut")
				self.set_proxy()
				self.test_proxy()
			except WebDriverException as e:
				self.driver.quit()
				print("-- {} no fue capas de conectarse en 10 segundos".format(self.actual_proxy["Ip"]))	
				self.proxy_list.modificateFunctionality(self.actual_proxy, "SomethingGoesWrong")
				self.configure_driver()
				self.driver = Firefox(capabilities=self.firefox_capabilities, options=self.options, firefox_profile=self.firefox_profile, executable_path='geckodriver')
				self.test_proxy()
				print("Algo salio mal: {}".format(e))
							
			print("!!!! > Tested {}".format(self.actual_proxy["Ip"]))

	def scrap(self):
		print("************************* Iniciando scrap ********************************")
		start_time = timeit.default_timer()
		try:
			self.driver.set_page_load_timeout(60)
			self.driver.get(self.url)
			self.test_content()
			self.test_captcha()

		except TimeoutException as e:
			print("-- {} no fue capas de conectarse en 60 segundos".format(self.actual_proxy["Ip"]))	
			self.proxy_list.modificateFunctionality(self.actual_proxy, "TimeOut")
			self.configure_driver()
			self.set_proxy()

		self.navigate()
		elapsed = timeit.default_timer() - start_time
		print("\n********************************************")
		print("***************** Time *********************")
		print("***************** {}".format(elapsed))
		print("********************************************\n")

		self.navigate()
		print("************************* Scrap Finalizado ********************************")




	def test_captcha(self):
		print("************************* Testando capcha")
		if self.main_strc["Captcha"] != "":
			try:
				captcha=self.driver.find_elements_by_css_selector('{}'.format(self.main_strc["Captha"]))
				print("*************************  Nos pescaron :) :) :) :) :) :) :) :)")
				self.proxy_list.modificateFunctionality(self.actual_proxy, "Captcha")
				self.set_proxy()
				self.driver.execute_script("location.reload()")
				self.navigate()
			except:
				raise

	def test_content(self):
		pass


	def navigate(self):
		pass
	


	def scrap(self):
		print("---> Iniciando el scrapp-----------")
		self.driver = Firefox(capabilities=self.firefox_capabilities, 
							  options=self.options, 
							  firefox_profile=self.firefox_profile, 
							  executable_path='geckodriver')
		self.set_proxy()
		self.driver.set_page_load_timeout(time_out)

		try:
			self.driver.get(self.url)
			self.navigate()
								

		except ValueError as e:
			print("\n**********************************************************************")
			print("\n{}".format(e))
			print("\n**********************************************************************")
			self.scrap()




				try:
					next = WebDriverWait(self.driver, 10).until(expected.element_to_be_clickable(
						(By.CSS_SELECTOR, '{}'.format(self.main_strc["Next"]["Dom"])))
					   )
					self.scrap()


	def navigate(self):
		if self.get_main_container():
			if self.get_unit_containers():
				
				if self.main_strc["Next"]["Dom"] != "":
					data = self.get_data("Next")
					if data != self.data:
						self.save(data, datafile)
						self.data = data
						self.next()
						self.navigate()
					else:
						print("Al parecer llegamos al final de los datos")

				elif self.main_strc["End"]["Dom"] != ""
					data = self.get_data("Scroll")
					if data != self.data:
					self.scroll()

			else:
				print("No se encontraron unidades de datos con la estructura dada, Finalizando")
		else:
			print("No se encontró el contenedor, la página pudo haber cambiado, o el antiscrapper nos detectó")


	def get_data(self, more_content_style, data_auto_delimter = self.data_auto_delimter):
		
		data = []
		self.data = []

		if more_content_style == "Next":
			for element in self.main_strc["ElCont"]["Elements"]:
				
				data_dict = {}
				for key, selector in self.data_strc.items(): 
					elements = element.find_elements_by_css_selector('{}'.format(selector))
					data_dict[key] = ""
					if elements != []:
						for e in elements:
							if insedesep==True:
								data_dict[key] += data_auto_delimter[0]+e.text+data_auto_delimter[1]
							else:
								data_dict[key] += e.text

				if "".join(list(data_dict.values())) != "":
					data.append(data_dict)

			return data



		if more_content_style == "Scroll":
			before_scroll = self.get_unit_containers()
			actions = ActionChains(scroll.driver)
			actions.move_to_element(element).perform(before_scroll[-1])
			after_scroll = self.get_unit_containers()
			if len(before_scroll) != len(after_scroll):
				data_dict = {}
				for element in before_scroll:
					data_dict = {}
					for key, selector in self.data_strc.items(): 
						elements = element.find_elements_by_css_selector('{}'.format(selector))
						data_dict[key] = ""
						if elements != []:
							for e in elements:
								if insedesep==True:
									data_dict[key] += data_auto_delimter[0]+e.text+data_auto_delimter[1]
								else:
									data_dict[key] += e.text

					if "".join(list(data_dict.values())) != "":
						data.append(data_dict)
					self.element.remove()
			self.get_data(more_content_style)


	def save_data(self, file):
		print("Guardando {} filas en: {}".format(len(self.data),file))
		with open(data_file, "a") as datafile:
			if "".join(list(data_dict.values())) != "":
				writer = csv.DictWriter(datafile, delimiter="\t", fieldnames=list(self.data_strc.keys()))
				for data_row in self.data:
					writer.writerow(data_row)
		print("Guardadas {} filas en: {}".format(len(self.data), file))
	'''