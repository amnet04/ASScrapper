from .ASScrapper import Scrapper
from .utilities.urlsGoogleNewsGenerator import urlsGenerator
import pytest
import random
import csv

"""def test_master():
    url  = 'http://www.google.com/search?q="alphabet+inc"&tbs=cdr%3A1%2Ccd_min%3A2%2F1%2F2020%2Ccd_max%3A2%2F1%2F2020&tbm=nws'
    prv =  Scrapper("GoogleNews",url, headless=False, str_folder="examples", str_file="GoogleNews.csv")

    prv.get_navigate("Google.csv")
    prv.open_dom()
    prv.configure_driver()
    prv.get_elements()
    prv.driver.close()"""


def test_url():
    proxy_list = []
    with open("scrapped/free-proxy-list.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            if row["Ip"] != '':
                proxy_list.append(dict(row))
    
    
    urls = urlsGenerator("'Alphabet Inc'", ['2019-01-01','2020-02-25'])
    prv =  Scrapper("GoogleNews_2019_01_01","", headless=True, str_folder="examples", str_file="GoogleNews.csv")
    prv.open_dom()
    for url in urls: 
        prv.configure_driver()
        proxy=random.choice(proxy_list)
        try:
            prv.ChangeProxy(proxy["Ip"] ,proxy["Port"])
        except:
            proxy=random.choice(proxy_list)
            prv.ChangeProxy(proxy["Ip"] ,proxy["Port"])
        prv.driver.get(url)
        prv.driver.implicitly_wait(random.randrange(1, int(random.random()*10)+2))
        prv.get_elements()
        prv.get_navigate("scrapped/Google.csv")

        change_proxy = random.randrange(1,11,1)
        if change_proxy > 8:
            print("cambiando proxy")
            proxy=random.choice(proxy_list)
            try:
                prv.ChangeProxy(proxy["Ip"] ,proxy["Port"])
            except:
                proxy=random.choice(proxy_list)
                prv.ChangeProxy(proxy["Ip"] ,proxy["Port"])
        prv.driver.close()
    