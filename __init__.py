import logging
from selenium.webdriver.remote.remote_connection import LOGGER


logging.basicConfig(filename="/tmp/scrapper.log",
					level=logging.INFO,
					format=' %(levelname)s - %(asctime)s - %(message)s')

LOGGER.setLevel(logging.WARNING)

logger = logging.getLogger('Scrapper')