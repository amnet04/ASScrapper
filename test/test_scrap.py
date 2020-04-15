import pytest
import random
import csv

from asscrapper import asscrapper as assc
from asscrapper.utilities.proxygetter import proxies
#from ..utilities.urlsGoogleNewsGenerator import urlsGenerator

# Configure files
import pathlib
thispath=pathlib.Path(__file__).parent.parent.absolute()



"""def test_proxy():
    print()
    prv =  proxies()
    prv.select_proxy()
    while len(prv.proxy_list)>0:
        prv.proxy_notwork(prv.selected_proxy.host,prv.selected_proxy.port)
        prv.select_proxy()"""
        

def test_scrap():
    print()
    prv = assc.Scrapper("AlphabetINC", 
                   [{"URL":"https://www.google.com/search?q=coronavirus&tbm=nws","PARAM":"Coronavirus"},
                    {"URL":"https://www.google.com/search?q='Alvaro Uribe'&tbm=nws","PARAM":"Alvaro Uribe"}], 
                   "/home/sarnahorn/Programacion/Doctorado/asscrapper/examples/GoogleNews.csv",
                   test_url = "http://ipv4.plain-text-ip.com/",
                   proxy = {"Types":['HTTP','HTTPS'], "Limit":30, "Countries":None},
                   max_nexts = 2)

  
    
    