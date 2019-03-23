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
        #print(soup_level1)

        print("\n\n")

        links = []

        for a in soup_level1.find_all('a'):
            #print(a)
            if str(a).startswith("<a class=\"nlink\" data-book=\"#eKGWB/"):
                links.append(a)

        print("\n\nlinks:")
        link_texts = []
        link_paths = []
        for s in links:
            print(s)
            link_texts.append(self.__get_link_text(s))
            link_paths.append(self.__get_link_adress(s, url))

        print("\n\nGot links to look for:\n")

        buttons = []
        for t in link_paths:
            print(t)

        print("\n\nButtons to check: {}".format(len(buttons)))

        driver.close()

        return 0

    def __get_link_text(self, tag):
        res = ""

        parts = str(tag).split('>')

        if len(parts) > 1:
            res = parts[1]

        parts = res.split('<')
        res = parts[0]

        return res

    def __get_link_adress(self, tag, url):
        res = ""
        url_prefix = str(url).split('#')[0]

        parts = str(tag).split('data-link=\"')

        if len(parts) > 1:
            res = parts[1]

        parts = res.split('\"')
        res = url_prefix + parts[0]

        return res
