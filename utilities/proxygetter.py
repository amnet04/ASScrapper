"""Find working proxies and use them concurrently.

Note: Pay attention to Broker.serve(), instead of the code listed below.
      Perhaps it will be much useful and friendlier.
"""
import asyncio
from proxybroker import Broker

class proxies():

    proxy_list = []

    def __init__(self, typ=['HTTP','HTTPS'], lim=5, countries_list=None):
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        tasks = asyncio.gather(
            broker.find(types=typ, limit=lim, countries=countries_list),
            self.show(proxies))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(tasks)

    async def show(self, proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None: break
            self.proxy_list.append(proxy)
