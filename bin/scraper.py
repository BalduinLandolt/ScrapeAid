import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
import os
from text import ScrapedText
import sys

# TODO check dithyramben

# TODO FF in jenseits von gut und böse (und anderen späteren?), sonst nicht... einheitlich!

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

    def scrape_cached_data(self):
        # TODO do stuff here
        return


    def download_from_url(self, url):
        """
        Run Scraper.

        :return: Exit code: 0 if successful; -1 if not.
        """

        print("Running Scraper...\n")

        exit_code = self.call_url(url)

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
        driver.set_window_rect(500, 140, 900, 600)

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

        print("\nloading...\n")

        time.sleep(1)
        threshold = 1
        max = len(link_paths)

        res_all = []
        texts = []

        start_time = time.time()

        for l in link_paths:
            i = link_paths.index(l)
            title = link_texts[i]
            prog = i / max
            t_delta = time.time() - start_time
            t_average = t_delta / (i + 1)

            sys.stdout.write("\r{} of {} ({} %)  ---  Running {} s so far... (ca. {} s remaining)".format(i, max, (100 * prog), round(t_delta, 2), round(t_average * (max - i), 2)))
            sys.stdout.flush()

            # for testing purposes
            #if i >= threshold:
            #    break

            #for testing purpose
            #if title != "Also sprach Zarathustra III":
            #    continue

            #print("Looking for '{}' in: {}".format(title, l))

            driver.get(l)
            driver.refresh()
            soup = BeautifulSoup(driver.page_source, 'lxml')

            #res = self.grab_text(driver, l)
            #txt = ScrapedText(title, res)
            #res_all.append(res)
            #texts.append(txt)
            #self.__save_to_file(txt)
            self.__save_orig_to_file(title, str(soup))
            #print("\nWaiting 1 second...\n")
            time.sleep(.6)

        driver.close()

        #print("\n\ngot {} texts:".format(len(texts)))
        #for t in texts:
        #    print(t.get_title())
        #    print("##################")

        # TODO check for exit code
        return 0

    def grab_text(self, driver, url):
        print("grabbing...")
        driver.get(url)
        driver.refresh()

        res_list = []

        soup = BeautifulSoup(driver.page_source, 'lxml')
        for div in soup.find_all('div'):
            if 'class' in div.attrs:
                if len(div.attrs['class']) > 0 and div.attrs['class'][0] == "txt_block":
                    sub_soup = BeautifulSoup(str(div), 'lxml')
                    for h in sub_soup.find_all('h1'):
                        res_list.append(h)
                    for h in sub_soup.find_all('h2'):
                        res_list.append(h)
                    for h in sub_soup.find_all('h3'):
                        res_list.append(h)
                    for h in sub_soup.find_all('h4'):
                        res_list.append(h)
                    for h in sub_soup.find_all('h5'):
                        res_list.append(h)
                    for h in sub_soup.find_all('h6'):
                        res_list.append(h)
                    for p in sub_soup.find_all('p'):
                        if p.has_attr('class') and len(p.attrs['class']) > 0 and p.attrs['class'][0] == "Untertitel":
                            wrapper = sub_soup.new_tag("div")
                            wrapper['class'] = 'p'
                            p.wrap(wrapper)
                    for sub_div in sub_soup.find_all('div'):
                        if len(sub_div.attrs['class']) > 0 and (sub_div.attrs['class'][0] == "p" or sub_div.attrs['class'][0] == "l"):
                            res_list.append(sub_div)

        print("scraped {}".format(url))
        print("got {} elements that might be containing text".format(len(res_list)))

        return res_list

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

    def __save_to_file(self, text):
        path = "data/output/" + text.get_title() + ".txt"

        #if not os.path.isfile(path):
        #    with open(path, "x") as f:
        #        print("Created File: {}".format(f))

        with open(path, "w+", encoding='utf-8') as f:
            f.write("$" + text.get_title())
            f.write("\n")
            #c = text.get_content()
            #for l in c:
            #    f.write(str(l) + "\n")
            f.write(text.get_content_string())

        return


    def __save_orig_to_file(self, title, str):
        path = "data/tmp/orig/" + title + ".html"

        #print("saving original data of {} to temporary file: {}".format(title, path))

        #if not os.path.isfile(path):
        #    with open(path, "x") as f:
        #        print("Created File: {}".format(f))

        with open(path, "w+", encoding='utf-8') as f:
            #f.write("$" + text.get_title())
            #f.write("\n")
            #c = text.get_content()
            #for l in c:
            #    f.write(str(l) + "\n")
            #f.write(text.get_content_string())
            f.write(str)

        return
