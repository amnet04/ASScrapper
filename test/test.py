from ..scrapper.ASScrapper import Scrapper
from ..utilities.urlsGoogleNewsGenerator import urlsGenerator
from ..utilities.freeProxyRotator import proxyRotator
import pytest
import random
import csv

import pathlib
thispath=pathlib.Path(__file__).parent.parent.absolute()

def rotate_url(urls, proxylist):
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
        prv.configure_driver()
        prv.driver.set_page_load_timeout(60)
        prv.url = url
        try:  
            prv.driver.get(prv.url)
        except:
            print("{} NO sirvio, a otro".format(prv.proxy))
            prv.driver.close()
            rotate_url(urls, proxylist)

        prv.driver.implicitly_wait(random.randrange(1, int(random.random()*10)+2))
        prv.get_elements()
        prv.get_navigate("{}/scrapped/Google.csv".format(thispath))


def test_url():

    proxylist = []
    with open("{}/{}".format(thispath,"scrapped/free-proxy-list.csv"), "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            if row["Ip"] != '':
                proxylist.append(dict(row))
    
    
    urls = urlsGenerator("'Alphabet Inc'", ['2019-01-01','2020-02-25'])
    rotate_url(urls, proxylist)


    
    
    