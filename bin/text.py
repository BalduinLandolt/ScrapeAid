from bs4 import BeautifulSoup

class ScrapedText:

    def __init__(self, title, content):
        self.__title = title
        self.__content = content
        self.__content_string = self.__tidy_content(content)

    def get_title(self):
        return self.__title

    def get_content(self):
        return self.__content

    def get_content_string(self):
        return self.__content_string

    def __tidy_content(self, content):
        res = ""

        for c in content:
            soup = BeautifulSoup(str(c), 'lxml')
            for br in soup.find_all('br'):
                br.replace_with("\n")
            for h in soup.find_all('h1'):
                h.insert_before("\n")
            for h in soup.find_all('h2'):
                h.insert_before("\n")
            for h in soup.find_all('h3'):
                h.insert_before("\n")
            for h in soup.find_all('h4'):
                h.insert_before("\n")
            for h in soup.find_all('h5'):
                h.insert_before("\n")
            for h in soup.find_all('h6'):
                h.insert_before("\n")
            while "Erratum" in soup.get_text():
                #print(soup)
                soup.find('em').parent.decompose()
            #for em in soup.find_all('em'):
            #    em.parent.decompose()
            res = res + soup.get_text() + "\n"

        #res = ""
        #for c in content:
        #    res = res + str(c) + "\n"

        return res
