import pytest
import random
import csv

#from ..scrapper.ASScrapper import Scrapper
from ..scrapper.asc import Scrapper
from ..utilities.urlsGoogleNewsGenerator import urlsGenerator


import pathlib

# Configure files
thispath=pathlib.Path(__file__).parent.parent.absolute()

def test():
    prv = Scrapper("Prv", 
                   [{"URL":"https://www.google.com/search?q=coronavirus&tbm=nws","PARAM":"Coronavirus"},
                    {"URL":"https://www.google.com/search?q=coronavirus&tbm=nws","PARAM":"Coronavirus"}], 
                   "/home/sarnahorn/Programacion/Doctorado/asscrapper/examples/free-proxy-list-dot_net.csv",
                   proxy = {"url":"https://free-proxy-list.net/", 
                            "str_file":"/home/sarnahorn/Programacion/Doctorado/asscrapper/examples/free-proxy-list-dot_net.csv",
                            "out_file":"/home/sarnahorn/Programacion/Doctorado/asscrapper/scrapped/free-proxy-list.csv"} )
"""
def rotate_proxy(prv):
    
    try:
        prv.driver.quit()
    except:
        print("Ya taba cerrao")

    prv.configure_driver()
    prv.driver.set_page_load_timeout(35)
    try:  
        prv.driver.get(prv.url)
        print("opteniendo elementos")
        prv.get_elements()
        w_time = random.randrange(1, int(random.random()*10)+2)
        print("Espera de {}".format(w_time))
        prv.driver.implicitly_wait(w_time)
        print("Fin de espera")
        prv.get_navigate("{}/scrapped/Google.csv".format(thispath))
    except:
        print("Tiempo de espera agotado")
        prv.DropProxyFromList()
        prv.driver.quit()
        prv.ChangeProxy()
        rotate_proxy(prv)

    


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

    for url in urls:
        print("URL: ", url)
        prv.url = url
        rotate_proxy(prv)
"""

    
    
    