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

    def run(self, url):
        """
        Run Scraper.

        :return: Exit code: 0 if successful; -1 if not.
        """

        print("Running Scraper...\n")

        exit_code = 0

        # TODO ckeck for exit code
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
        driver.set_window_rect(600, 10, 1000, 800)

        print("Browser open.\nDoing stuff now...")

        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        print("\n\nGot HTML:\n\n")
        #print(soup)

        #print("\n\n")

        links = []

        for a in soup.find_all('a'):
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

        for t in link_paths:
            print(t)

        time.sleep(1)
        max = 1

        for l in link_paths:
            i = link_paths.index(l)
            title = link_texts[i]
            # TODO remove max clause to get all
            if i >= max:
                break
            print("Looking for '{}' in: {}".format(title, l))
            res = self.grab_text(driver, l)
            # TODO Store result
            print("Waiting 1 second...")
            time.sleep(1)

        driver.close()

        return 0

    def grab_text(self, driver, url):
        res = ""

        print("Should be grabbin' stuff here\n\n")
        driver.get(url)
        driver.refresh()

        soup = BeautifulSoup(driver.page_source, 'lxml')
        for div in soup.find_all('div'):
            if 'class' in div.attrs:
                if len(div.attrs['class']) > 0 and div.attrs['class'][0] == "txt_block":
                    sub_soup = BeautifulSoup(str(div))
                    # TODO read h2 etc. here
                    for sub_div in sub_soup.find_all('div'):
                        if len(sub_div.attrs['class']) > 0 and sub_div.attrs['class'][0] == "p":
                            print(sub_div.attrs)
                            print(sub_div)
                            print("\n\n------------\n\n")

        # TODO store result from driver

        return res

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
