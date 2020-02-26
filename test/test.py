from ..scrapper.ASScrapper import Scrapper
from ..utilities.urlsGoogleNewsGenerator import urlsGenerator
from ..utilities.freeProxyRotator import proxyRotator
import pytest
import random
import csv

import pathlib
thispath=pathlib.Path(__file__).parent.parent.absolute()

def rotate_proxy(prv):
    
    try:  
        prv.driver.get(prv.url)
    except:
        prv.DropProxyFromList()
        prv.driver.close()
        prv.ChangeProxy()
        rotate_proxy(prv)

    w_time = random.randrange(1, int(random.random()*10)+2)
    print("Espera de {}".format(w_time))
    prv.driver.implicitly_wait(w_time)
    print("Fin de espera")
    prv.get_elements()
    prv.get_navigate("{}/scrapped/Google.csv".format(thispath))


def test_url():

    proxylist = proxyRotator()
    
    
    urls = urlsGenerator("'Alphabet Inc'", ['2019-01-01','2020-02-25'])

    prv =  Scrapper("GoogleNews_2019_01_01",
                    "", 
                    headless=False, 
                    str_folder="{}/{}".format(thispath,"examples"), 
                    proxy_list = proxylist,
                    str_file="GoogleNews.csv")
    prv.open_dom()
    prv.configure_driver()
    for url in urls:
        print("URL: ", url)
        prv.driver.set_page_load_timeout(20)
        prv.url = url
        rotate_proxy(prv)


    
    
    