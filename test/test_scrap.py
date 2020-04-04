import pytest
import random
import csv

from asscrapper import asscrapper as assc
#from ..utilities.urlsGoogleNewsGenerator import urlsGenerator

# Configure files
import pathlib
thispath=pathlib.Path(__file__).parent.parent.absolute()

proxy_list1 = [[{"URL":"https://free-proxy-list.net/", "PARAM":"frre-proxy"}],
                "/home/sarnahorn/Programacion/Doctorado/asscrapper/examples/free-proxy-list-dot_net.csv",
                "/home/sarnahorn/Programacion/Doctorado/asscrapper",
                False
              ]

proxy_list2 = [[{"URL":"https://www.proxynova.com/proxy-server-list/elite-proxies/","PARAM":"ProxynovaElite"}], 
               "/home/sarnahorn/Programacion/Doctorado/asscrapper/examples/proxynova.csv",
               "/home/sarnahorn/Programacion/Doctorado/asscrapper",
               True
               ] 

proxy_list3 = [[{"URL":"https://www.proxynova.com/proxy-server-list/anonymous-proxies/","PARAM":"ProxynovaAnonimus"}], 
               "/home/sarnahorn/Programacion/Doctorado/asscrapper/examples/proxynova.csv",
               "/home/sarnahorn/Programacion/Doctorado/asscrapper",
               True
               ] 


"""def test_proxy():
    prv = fpr.scrappedProxyList(proxy_list2[0],proxy_list2[1],proxy_list2[2],True)
    proxies = prv.getUtilProxies()
    prv.modificateFunctionality(proxies[0], "TimeOut")
    prv.modificateFunctionality(proxies[0], "TimeOut")
    proxies = prv.getUtilProxies()"""


def test_scrap():
    print()
    prv = assc.Scrapper("AlphabetINC", 
                   [{"URL":"https://www.google.com/search?q=coronavirus&tbm=nws","PARAM":"Coronavirus"},
                    {"URL":"https://www.google.com/search?q='Alvaro Uribe'&tbm=nws","PARAM":"Alvaro Uribe"}], 
                   "/home/sarnahorn/Programacion/Doctorado/asscrapper/examples/GoogleNews.csv",
                   proxy = False,
                   max_nexts = 0)



    
    
    