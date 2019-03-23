import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
import os


class Scraper:
    """
    Class 'Scraper' that does all the scraping.
    """

    def __init__(self):
        """
        Constructor for the 'Scraper' Class.
        """

        print("Initialized an instance of Scraper")
        return

    def run(self):
        """
        Run Scraper.

        :return: Exit code: 0 if successful; -1 if not.
        """

        print("Running Scraper...\n")

        exit_code = 0

# TODO do stuff here

# TODO Test URL. Should be solved by dynamic input
        url = "http://www.nietzschesource.org/#eKGWB/"
        self.call_url(url)

        return exit_code

    def call_url(self, url):
        """

        :param url:
        :return:
        """

        print("calling: {}".format(url))
        print("Opening browser...")

        driver = webdriver.Firefox()
        driver.implicitly_wait(30)

        print("Browser open.\nDoing stuff now...")

        driver.get(url)

        soup_level1 = BeautifulSoup(driver.page_source, 'html')
        print("\n\nGot HTML:\n\n")
        print(soup_level1)

        #driver.close()

        return 0
