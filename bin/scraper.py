import requests
import urllib.request
import time
from bs4 import BeautifulSoup


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

    def call_url(self, url):
        """

        :param url:
        :return:
        """

        print("calling: {}".format(url))

        return 0

    def run(self):
        """
        Run Scraper.

        :return: Exit code: 0 if successful; -1 if not.
        """

        print("Running Scraper...\n")

        exit_code = 0

# TODO do stuff here

# TODO Test URL. Should be solved by dynamic input
        url = "http://www.nietzschesource.org/"
        self.call_url(url)

        return exit_code
