import logging
import csv
from time import sleep
from os import path
import datetime
import random



# Selenium
import selenium.common.exceptions
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

"""logging.basicConfig(filename="scrapper.log",
                    level=logging.DEBUG,
                    format='%(asctime)s - %(message)s')"""


class Scrapper():


    def __init__(self, 
                 name, 
                 url, 
                 str_folder="", 
                 str_file="",
                 headless= False, 
                 wait=1):
        self.name = name
        self.url =  url
        self.str_file = str_file
        self.str_folder = str_folder
        self.main_str = {}
        self.data_str = {}
        self.data = []
        self.headless = headless
        self.wait = wait

       

    def configure_driver(self):
        if self.headless:
            options = Options()
            options.add_argument('-headless')
            self.driver = Firefox(executable_path='geckodriver', options=options)
        
        
        else:
            firefox_profile = FirefoxProfile()
            firefox_profile.set_preference('permissions.default.image', 2)
            firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
            firefox_profile.set_preference('media.navigator.video.enabled',False)
            firefox_profile.set_preference('media.encoder.webm.enabled',False)
            firefox_profile.set_preference('media.ffmpeg.enabled',False)
            firefox_profile.set_preference('media.flac.enabled',False)
            self.driver = Firefox(firefox_profile=firefox_profile)

        
    def open_dom(self):
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



    def get_elements(self):
        self.main_str["LiCont"]["Elements"] = self.driver.find_elements_by_css_selector('{}'.format(self.main_str["LiCont"]["Dom"]))
        self.main_str["ElCont"]["Elements"] = []
        
        
        if self.main_str["LiCont"]["Elements"] != []:
            for element in self.main_str["LiCont"]["Elements"]:
                self.main_str["ElCont"]["Elements"] += element.find_elements_by_css_selector('{}'.format(self.main_str["ElCont"]["Dom"]))
        
        
    def get_data(self, data_file):
        if not path.isfile(data_file):
            with open(data_file, "w") as datafile:
                writer = csv.DictWriter(datafile, delimiter="\t", fieldnames=list(self.data_str.keys()))
                writer.writeheader()
            
        if self.main_str["ElCont"]["Elements"] != []:       
            for element in self.main_str["ElCont"]["Elements"]:
                data_dict = {}
                for key, selector in self.data_str.items(): 
                    elements = element.find_elements_by_css_selector('{}'.format(selector))
                    data_dict[key] = ""
                    if elements != []:
                        for e in elements:
                            data_dict[key] += "<e>"+e.text+"</e>"
                
                with open(data_file, "a") as datafile:
                    writer = csv.DictWriter(datafile, delimiter="\t", fieldnames=list(self.data_str.keys()))
                    writer.writerow(data_dict)

        else:
            raise("Element container doesnt find")
    


    def get_navigate(self, data_file):
        sleep(random.randrange(2, 5+int(random.random()*10)))
        if self.main_str["Next"]["Dom"] != "":
            self.get_elements()
            self.get_data(data_file)
            try:
                self.main_str["Next"]["Elements"] = self.driver.find_element_by_css_selector('{}'.format(self.main_str["Next"]["Dom"]))
                self.main_str["Next"]["Elements"].click()
                self.get_navigate(data_file)
            except:
                print("Data recovery ends", end = "\r")

        elif self.main_str["End"]["Elements"]:
            self.main_str["End"]["Elements"] = self.driver.find_element_by_css_selector('{}'.format(self.main_str["End"]["Dom"]))
            pass
    
        else:
           self.get_data(data_file) 
