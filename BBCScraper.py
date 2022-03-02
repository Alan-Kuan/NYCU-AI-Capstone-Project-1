#! /usr/bin/env python3
import os
import time
import requests
from bs4 import Tag, BeautifulSoup as bs
from requests.api import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

base_url = "https://www.bbc.com/news"

class BBCScraper:
    def __init__(self, url: str) -> None:
        page = requests.get(url)
        soup = bs(page.content, "html.parser")
        self.__body = soup.find("article")
        self.title = self.__get_title()
        self.content = self.__get_content()

    def __get_title(self) -> str:
        assert isinstance(self.__body, Tag)
        title = self.__body.find(id="main-heading")
        assert isinstance(title, Tag)
        return title.text

    def __get_content(self) -> str:
        assert isinstance(self.__body, Tag)
        text_blocks = self.__body.select("div[data-component='text-block']")
        return ' '.join([b.text for b in text_blocks])

def get_news(categories: list,
             news_per_category: int,
             driver: webdriver.Chrome) -> dict:
    news = {}

    for category in categories:
        print(f"{ category }:")
        news[category] = []
        news_count = 0

        driver.get(f"{ base_url }/{ category.replace('-', '_and_') }")
        index_page = driver.find_element(by=By.ID, value="index-page")
        links = index_page.find_elements(by=By.TAG_NAME, value="a")
        for link in links:
            url = link.get_attribute("href")
            # this is a video news
            try:
                link.find_element(by=By.TAG_NAME, value="span")
            # this is a regular news
            except NoSuchElementException:
                if url.startswith(f"{ base_url }/{ category }-") and url not in news[category]:
                    news[category].append(url)
                    news_count += 1

        print(f"Total { news_count } articles were collected from #index-page.")

        time.sleep(1)

        # close the pop-up modal if it appears
        try:
            close_btn = driver.find_element(by=By.CLASS_NAME, value="tp-close.tp-active")
            close_btn.click()
        except NoSuchElementException:
            pass

        while news_count < news_per_category:
            ol = driver.find_element(by=By.TAG_NAME, value="ol")
            lis = ol.find_elements(by=By.CSS_SELECTOR, value="ol > li")
            for li in lis:
                article = li.find_element(by=By.TAG_NAME, value="article")
                link = article.find_element(by=By.TAG_NAME, value="a")
                url = link.get_attribute("href")
                # this is a video news
                try:
                    article.find_element(by=By.CLASS_NAME, value="smp-embed")
                    print(f"Skipped { url }.")
                # this is a regular news
                except NoSuchElementException:
                    if url.startswith(f"{ base_url }/{ category }-") and url not in news[category]:
                        news[category].append(url)
                        news_count += 1
                    if news_count == news_per_category:
                        break

            print(f"Total { news_count } articles has been collected so far.")

            next_btn = driver.find_element(by=By.CLASS_NAME, value="qa-pagination-next-page")
            next_btn.click()
            time.sleep(1)

        time.sleep(0.5)

    return news

if __name__ == "__main__":
    options = Options()
    options.add_argument("headless")
    service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = webdriver.Chrome(service=service, options=options)

    categories = [
        "business",
        "entertainment-arts",
        "science-environment",
        "technology"
    ]
    news = get_news(categories, 50, driver)

    driver.close()

    for category, urls in news.items():
        if not os.path.exists(category):
            os.mkdir(category)

        for idx, url in enumerate(urls):
            scraper = BBCScraper(url)
            title = scraper.title
            content = scraper.content

            with open(f"{ category }/{ idx }.txt", "w") as file:
                file.write(title)
                file.write('\n')
                file.write(content)
                print(f"{ category }/{ idx }.txt was created.")

            time.sleep(0.5)
