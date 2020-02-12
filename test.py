from .ASScrapper import Scrapper
import pytest

def test_master():
    url  = 'http://www.google.com/search?q="alphabet+inc"&tbs=cdr%3A1%2Ccd_min%3A2%2F1%2F2020%2Ccd_max%3A2%2F1%2F2020&tbm=nws'
    prv =  Scrapper("GoogleNews",url, headless=False, str_folder="examples", str_file="GoogleNews.csv")

    prv.get_navigate("Google.csv")
    #prv.driver.close()

    #https://www.google.com/search?q=alphabet+inc&biw=949&bih=686&source=lnt&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2019%2Ccd_max%3A1%2F1%2F2019&tbm=nws