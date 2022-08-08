from typing import List

from selenium import webdriver
from selenium.webdriver.common.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumDriver:

    def __init__(self, options: List[str] = []):
        self.options = options
        self.driver = self.init_driver()


    def init_driver(self):
        chrome_options = webdriver.ChromeOptions()

        for option in self.options:
            chrome_options.add_argument(option)

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        return driver
