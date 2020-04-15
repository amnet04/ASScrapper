import asyncio
from proxybroker import Broker
from asscrapper import logger
from time import sleep

class proxies():

    proxy_list = []
    selected_proxy = False

    def __init__(self, typ=['HTTP','HTTPS'], lim=15, countries_list=None):
        self.types = typ
        self.limit = lim
        self.countries_list = countries_list
        self.consults = 0
        self.retries = 0
        self.get_proxies()
        print("pl : ",self.proxy_list)
        print("pll: ",len(self.proxy_list))

    def get_proxies(self):
        self.consults += 1
        if self.consults < 10:
            try:
                logger.info("ProxyGetter: ---> Starting to get proxies")
                proxies = asyncio.Queue()
                broker = Broker(proxies)
                tasks = asyncio.gather(broker.find(types=self.types, 
                                                   limit=self.limit, 
                                                   countries=self.countries_list),
                                       self.append_proxies(proxies))
                loop = asyncio.get_event_loop()
                loop.run_until_complete(tasks)
                self.retries = 0
            except  RuntimeError:
                self.retries += 1
                logger.info("ProxyGetter: ---> Getproxy fail, waiting {} to the next try".format(5*self.retries))
                sleep(5*self.retries)
                self.get_proxies()
        else:
            sleep(5)
            self.get_proxies()


    def proxy_notwork(self, host, port):
        logger.info("ProxyGetter: -----> Proxies in list before : {} ".format(len(self.proxy_list)))
        if len(self.proxy_list) > 0:
            for proxy in self.proxy_list:
                if proxy.host == host  and proxy.port == port:
                    logger.info("ProxyGetter: ---> {} doesn't work, deleting".format(host))
                    self.proxy_list.remove(proxy)
            logger.info("ProxyGetter: -----> Proxies in list after : {} ".format(len(self.proxy_list)))

    def select_proxy(self):
        if len(self.proxy_list) > 0:
            if self.proxy_list[0].is_working:
                self.selected_proxy = self.proxy_list[0]
                logger.info("ProxyGetter: ---> {} selected".format(self.selected_proxy.host))
            else:
                logger.info("ProxyGetter: ---> {} reported as not working, deleting".format(self.selected_proxy.host))
                self.proxy_list.remove(proxy)
                self.select_proxy()
        else:
            logger.info("ProxyGetter: ---> Proxies list exhausted")
            self.get_proxies()
            self.select_proxy()


    async def append_proxies(self, proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None: break
            self.proxy_list.append(proxy)
