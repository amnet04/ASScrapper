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
        self.limit = 0
       

    def configure_driver(self):
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
            self.driver = Firefox(capabilities=self.firefox_capabilities, options=self.options, firefox_profile=self.firefox_profile, executable_path='geckodriver')
        
        
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
            self.driver = Firefox(capabilities=self.firefox_capabilities, options=self.options, firefox_profile=self.firefox_profile, executable_path='geckodriver')

        

        
    def open_dom(self):
        try:
            filename = "{}/{}".format(self.str_folder,self.str_file)
            with open(filename, "r") as csvfile:
                data_str = csv.DictReader(csvfile, delimiter="\t")
                if data_str.fieldnames == ["Data", "Dom"]:
                    data_str = [dict(x) for x in list(data_str)]
                    if [x["Data"] for x in data_str[0:5]] == ["LiCont", "ElCont", "Next", "End", "Captcha"]: 
                        for data in data_str[0:5]:
                            self.main_str[data["Data"]] = {"Dom":data["Dom"]}
                        for data in data_str[5:]:
                            self.data_str[data["Data"]] = data["Dom"]
                    else:
                        raise ValueError("The first 4 rows must be: 'LiCont', 'ElCont', 'Next', and 'End'")
                else:
                    raise ValueError("csvfile header doesnt match!!!!")

        except IOError as e:
            raise(e)



    def get_elements(self, limit=0, insedesep=True):

        print(self.main_str["LiCont"]["Dom"])
        WebDriverWait(self.driver, 30).until(expected.visibility_of_element_located((By.CSS_SELECTOR, '{}'.format(self.main_str["LiCont"]["Dom"]))))
        self.main_str["LiCont"]["Elements"] = self.driver.find_elements_by_css_selector('{}'.format(self.main_str["LiCont"]["Dom"]))
        self.main_str["ElCont"]["Elements"] = []
        
        
        if self.main_str["LiCont"]["Elements"] != []:
            for element in self.main_str["LiCont"]["Elements"]:
                self.main_str["ElCont"]["Elements"] += element.find_elements_by_css_selector('{}'.format(self.main_str["ElCont"]["Dom"]))
        
        else:
            print ("Element container doesnt find, probablemente nos agarraron")
            self.driver.quit()            
            self.DropProxyFromList()
            self.ChangeProxy()
            self.configure_driver()
            self.driver.get(self.url)
            self.get_navigate(data_file, limit=limit, insedesep=insedesep)


        
    def get_data(self, data_file, limit=0,insedesep=True):
        if not path.isfile(data_file):
            with open(data_file, "w") as datafile:
                writer = csv.DictWriter(datafile, delimiter="\t", fieldnames=list(self.data_str.keys()))
                writer.writeheader()
            
        if self.main_str["ElCont"]["Elements"] != []: 
            print(len(self.main_str["ElCont"]["Elements"]), "Elementos encontrados en", self.url)      
            for element in self.main_str["ElCont"]["Elements"]:
                data_dict = {}
                for key, selector in self.data_str.items(): 
                    elements = element.find_elements_by_css_selector('{}'.format(selector))
                    data_dict[key] = ""
                    if elements != []:
                        for e in elements:
                            if insedesep==True:
                                data_dict[key] += "<e>"+e.text+"</e>"
                            else:
                                data_dict[key] += e.text
                
                with open(data_file, "a") as datafile:
                    if "".join(list(data_dict.values())) != "":
                        writer = csv.DictWriter(datafile, delimiter="\t", fieldnames=list(self.data_str.keys()))
                        writer.writerow(data_dict)

        else:
            print ("Element container doesnt find, probablemente nos agarraron")
            self.driver.quit()            
            self.DropProxyFromList()
            self.ChangeProxy()
            self.configure_driver()
            self.driver.get(self.url)
            self.get_navigate(data_file, limit=limit, insedesep=insedesep)

    


    def get_navigate(self, data_file, limit=0,  insedesep=True):
        print("navegando")
        self.limit += 1
        sleep(random.randrange(2, 5+int(random.random()*10)))
        if self.main_str["Next"]["Dom"] != "":
            print("Chequeo de límites", self.limit, limit)
            self.get_elements(limit=limit,  insedesep=insedesep)
            self.get_data(data_file, limit, insedesep)
            try:
                if  limit == 0 or  self.limit < limit :
                    self.main_str["Next"]["Elements"] = WebDriverWait(self.driver, 2).until(expected.element_to_be_clickable((By.CSS_SELECTOR, '{}'.format(self.main_str["Next"]["Dom"]))))
                    self.main_str["Next"]["Elements"].click()
                    self.get_navigate(data_file, limit, insedesep)

            except:
                print("Data recovery ends")
                self.driver.quit()
                
        elif self.main_str["End"]["Elements"]:
            self.main_str["End"]["Elements"] = self.driver.find_element_by_css_selector(self.main_str["End"]["Dom"])
            self.get_data(data_file, limit, insedesep)
            print("Fin")
            self.driver.quit()
    
        else :
           self.get_data(data_file, limit, insedesep)
           print("Else")
           self.driver.quit()
        


    def ChangeProxy(self):
        
        self.limit = 0
        if self.proxy_list:
            if len(self.proxy_list) > 1:

                self.proxy = random.choice(self.proxy_list)
                print("Cambiando proxy a ",self.proxy["Ip"])
                self.firefox_capabilities['marionette'] = True

                self.firefox_capabilities['proxy'] = {
                    "proxyType": "MANUAL",
                    "httpProxy": "{}:{}".format(self.proxy["Ip"],self.proxy["Port"]),
                    "ftpProxy": "{}:{}".format(self.proxy["Ip"],self.proxy["Port"]),
                    "sslProxy": "{}:{}".format(self.proxy["Ip"],self.proxy["Port"])
                }
            else:
                print("Se acabaron las opciones, pidiendo mas proxys")
                self.LoadProxyList()
                self.ChangeProxy()
            try:
                self.driver.quit()
            except:
                print("Ya ta Cerrado")
            self.driver = Firefox(capabilities=self.firefox_capabilities, options=self.options, firefox_profile=self.firefox_profile)
        

    def LoadProxyList(self):
        from ..utilities.freeProxyRotator import proxyRotator
        self.proxy_list = proxyRotator()

    def DropProxyFromList(self):
        try:
            print("{} NO sirvio dentro, se borra".format(self.proxy["Ip"]))
            self.proxy_list.remove(self.proxy)
        except:
            print("ya se había borrado")
        print("Quedan {}".format(len(self.proxy_list)))