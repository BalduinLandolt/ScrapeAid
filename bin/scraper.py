import time
from bs4 import BeautifulSoup
from selenium import webdriver
import os
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

        self.soups_orig = None
        self.soups_textblock = None

        print("Initialized an instance of Scraper")
        return

    def scrape_data_from_textblock_to_minimalist(self):
        if self.soups_textblock is None:
            self.__load_cached_textblocks()

        self.strip_textblock_to_minimalist(self.soups_textblock)
        return

    def strip_textblock_to_minimalist(self, l):
        for text in l:
            title = text.html['filename']
            html_string = ""
            #TODO adjust
            #for div in text.find_all('div'):
            #    if 'class' in div.attrs and len(div.attrs['class']) > 0 and div.attrs['class'][0] == "txt_block":
            #        html_string = html_string + str(div)
            #self.__cache_text_block(title, html_string)
        return

    def scrape_data_from_orig_to_textblocks(self):
        if self.soups_orig is None:
            self.__load_cached_origs()

        self.cache_text_blocks(self.soups_orig)

        # TODO do stuff here
        return

    def cache_text_blocks(self, l):
        for text in l:
            title = text.html['filename']
            html_string = ""
            for div in text.find_all('div'):
                if 'class' in div.attrs and len(div.attrs['class']) > 0 and div.attrs['class'][0] == "txt_block":
                    html_string = html_string + str(div)
            self.__cache_text_block(title, html_string)
        return

    def download_from_url(self, url):
        """
        Run Scraper.

        :return: Exit code: 0 if successful; -1 if not.
        """

        print("Running Scraper...\n")

        self.call_url(url)

        return

    def call_url(self, url):
        """

        :param url:
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

        links = []

        for a in soup.find_all('a'):
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

        self.soups_orig = []

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

            driver.get(l)
            driver.refresh()
            soup = BeautifulSoup(driver.page_source, 'lxml')

            self.soups_orig.append(soup)
            self.__save_orig_to_file(title, str(soup))
            time.sleep(.6)

        driver.close()

        return

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

        with open(path, "w+", encoding='utf-8') as f:
            f.write("$" + text.get_title())
            f.write("\n")
            f.write(text.get_content_string())

        return

    def __save_orig_to_file(self, title, str):
        path = "data/tmp/orig/" + title + ".html"

        with open(path, "w+", encoding='utf-8') as f:
            f.write(str)

        return

    def __cache_text_block(self, title, html_string):
        if self.soups_textblock is None:
            self.soups_textblock = []

        path = "data/tmp/textblocks/" + title + ".html"
        soup = BeautifulSoup(html_string, 'lxml')
        self.soups_textblock.append(soup)

        with open(path, "w+", encoding='utf-8') as f:
            f.write(str(soup))

        print("Cached Textblock for: {}".format(path))

        return

    def __load_cached_origs(self):
        if self.soups_orig is None:
            self.soups_orig = []

        files = os.listdir("data/tmp/orig")

        for file in files:
            path = "data/tmp/orig/" + file
            if os.path.isfile(path):
                with open(path, "r+", encoding='utf-8') as f:
                    file_str = f.read()
                    s = BeautifulSoup(file_str, 'lxml')
                    s.html['filename'] = file.split('.')[0]
                    self.soups_orig.append(s)
            print("Read {} of {} Files from Cache".format(files.index(file) + 1, len(files)))

        return

    def __load_cached_textblocks(self):
        if self.soups_textblock is None:
            self.soups_textblock = []

        files = os.listdir("data/tmp/textblocks")

        for file in files:
            path = "data/tmp/textblocks/" + file
            if os.path.isfile(path):
                with open(path, "r+", encoding='utf-8') as f:
                    file_str = f.read()
                    s = BeautifulSoup(file_str, 'lxml')
                    s.html['filename'] = file.split('.')[0]
                    self.soups_textblock.append(s)
            print("Read {} of {} Files from Cache".format(files.index(file) + 1, len(files)))

        return
