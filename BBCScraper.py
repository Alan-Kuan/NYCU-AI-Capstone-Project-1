#! /usr/bin/env python3
import time
import requests
import bs4
from bs4 import BeautifulSoup as bs

base_url = "https://www.bbc.com"

class BBCScraper:
    def __init__(self, url: str) -> None:
        page = requests.get(url)
        soup = bs(page.content, "html.parser")
        self.__body = soup.find("article")
        self.title = self.__get_title()
        self.content = self.__get_content()

    def __get_title(self) -> str:
        assert isinstance(self.__body, bs4.Tag)
        title = self.__body.find(id="main-heading")
        assert isinstance(title, bs4.Tag)
        return title.text

    def __get_content(self) -> str:
        assert isinstance(self.__body, bs4.Tag)
        text_blocks = self.__body.select("div[data-component='text-block']")
        return ' '.join([b.text for b in text_blocks])

def get_news():
    pass

if __name__ == "__main__":
    scraper = BBCScraper('https://www.bbc.com/news/business-60300079')
    title = scraper.title
    content = scraper.content

    print(title)
    print(content)
