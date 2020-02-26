import logging
import csv
from time import sleep
from os import path
import datetime
import random



# Selenium
import selenium.common.exceptions
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

class Scrapper():

    def __init__(self, 
                 name, 
                 url, 
                 str_folder="", 
                 str_file="",
                 proxy_list = [],
                 headless= False, 
                 wait=1):

        self.name = name
        self.url =  url
        self.str_file = str_file
        self.str_folder = str_folder
        self.main_str = {}
        self.data_str = {}
        self.data = []
        self.proxy_list = proxy_list
        self.headless = headless
        self.wait = wait
        self.max_next = 0
        self.time_out = 35
        self.configure_driver()
        self.open_dom()


    def configure_driver(self):
    	print("\n\n\nConfigurando el driver -----------------------")

        self.firefox_capabilities = DesiredCapabilities.FIREFOX
        
        if self.proxy_list:
            if len(self.proxy_list) > 1:

                self.proxy = random.choice(self.proxy_list)
                self.proxy_list.remove(self.proxy)
                self.firefox_capabilities['marionette'] = True

                self.firefox_capabilities['proxy'] = {
                    "proxyType": "MANUAL",
                    "httpProxy": "{}:{}".format(self.proxy["Ip"],self.proxy["Port"]),
                    "ftpProxy": "{}:{}".format(self.proxy["Ip"],self.proxy["Port"]),
                    "sslProxy": "{}:{}".format(self.proxy["Ip"],self.proxy["Port"])
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

    def open_dom(self):
    	print("---> Configurando el dom -----------")
        try:
            filename = "{}/{}".format(self.str_folder,self.str_file)
            with open(filename, "r") as csvfile:
                data_str = csv.DictReader(csvfile, delimiter="\t")
                if data_str.fieldnames == ["Data", "Dom"]:
                    data_str = [dict(x) for x in list(data_str)]
                    if [x["Data"] for x in data_str[0:4]] == ["LiCont", "ElCont", "Next", "End"]: 
                        for data in data_str[0:4]:
                            self.main_str[data["Data"]] = {"Dom":data["Dom"]}
                        for data in data_str[4:]:
                            self.data_str[data["Data"]] = data["Dom"]
                    else:
                        raise ValueError("The first 4 rows must be: 'LiCont', 'ElCont', 'Next', and 'End'")
                else:
                    raise ValueError("csvfile header doesnt match!!!!")

        except IOError as e:
            raise(e)

    def scrap(self):
    	print("---> Iniciando el scrapp-----------")
    	self.driver = Firefox(capabilities=self.firefox_capabilities, 
    						  options=self.options, 
    						  firefox_profile=self.firefox_profile, 
    						  executable_path='geckodriver')
    	self.driver.set_page_load_timeout(time_out)

    	try:
    		self.driver.get(self.url)
    		
    		if self.get_main_container():
    			if self.get_unit_containers():
    				data = self.get_data()
    				if data != self.data:
    					self.save(data, datafile)
    					self.data = data

    				if self.main_str["Next"]["Dom"] != "":
    					self.next()

    				elif self.main_str["End"]["Dom"] != ""
    					self.scroll()

                    

    	except ValueError as e:
    		print("\n**********************************************************************")
    		print("\n{}".format(e))
    		print("\n**********************************************************************")
    		self.scrap()




    			try:
    				next = WebDriverWait(self.driver, 10).until(expected.element_to_be_clickable(
    					(By.CSS_SELECTOR, '{}'.format(self.main_str["Next"]["Dom"])))
    				   )
    				self.scrap()


            