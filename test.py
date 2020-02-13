from .ASScrapper import Scrapper
from .utilities.urlsGoogleNewsGenerator import urlsGenerator
import pytest

"""def test_master():
    url  = 'http://www.google.com/search?q="alphabet+inc"&tbs=cdr%3A1%2Ccd_min%3A2%2F1%2F2020%2Ccd_max%3A2%2F1%2F2020&tbm=nws'
    prv =  Scrapper("GoogleNews",url, headless=False, str_folder="examples", str_file="GoogleNews.csv")

    prv.get_navigate("Google.csv")
    prv.open_dom()
    prv.configure_driver()
    prv.get_elements()
    prv.driver.close()"""


def test_url():
    urls = urlsGenerator("'Alphabet Inc'", ['2019-01-01','2020-02-13'])
    for url in urls:
        prv =  Scrapper("GoogleNews",url, headless=False, str_folder="examples", str_file="GoogleNews.csv")
        prv.open_dom()
        prv.configure_driver()
        prv.get_elements()
        prv.get_navigate("scrapped/Google.csv")
        prv.close()
    