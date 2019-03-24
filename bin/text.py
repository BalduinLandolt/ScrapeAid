class ScrapedText:

    def __init__(self, title, content):
        self.__title = title
        self.__content = content

    def get_title(self):
        return self.__title

    def get_content(self):
        return self.__content
