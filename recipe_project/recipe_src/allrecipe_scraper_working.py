import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver
import selenium
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException, ElementNotVisibleException, WebDriverException
import numpy as np
import string
from collections import defaultdict
from pymongo import MongoClient
import json
import pickle

"""
Initializing mongodb
"""
client = MongoClient('mongodb://localhost:27017/')
db = client.vegetarian_ratings
collections = db['veggie_ratings']
# db = client.allrecipes
# collections = db['recipe_ratings']  drop this database later if new scraper works


def main(filename):
    """
    Open pickled list file for recipes and passes each link to the scraper
    """
    with open(filename, 'rb') as f:
        link_list = pickle.load(f)
    counter = 0
    link_list = link_list[::-1]
    for link in link_list[1000:]:
        weblink = "http://allrecipes.com" + link
        counter += 1
        scraper(weblink)
        if counter // 100 == counter / 100:
            time.sleep(30)
        print('Counts = {}'.format(counter))


def scraper(weblink):
    time.sleep(1)
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=800x841')
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(weblink)
    driver.implicitly_wait(10)
    """
    Revealing more reviews - will click 10 times unless the number of reviews
    is less than 120 then it stops and continues.  Exceptions will kick out of the loop
    and continue scraper - these are all the exceptions that were thrown upon testing
    the code.
    """
    for n in range(10):
        try:
            clicker = driver.find_element_by_css_selector(
                 '#reviews > div.recipe-reviews__more-container > div.more-button'
                )
            clicker.location_once_scrolled_into_view
            clicker.click()
            time.sleep(1)
        except (TimeoutException, NoSuchElementException, InvalidSelectorException, ElementNotVisibleException, WebDriverException):
            break
    """ method to grab relevant info from the visible reviews """
    html = driver.page_source
    soup_scraper(weblink, html)
    driver.quit()


def soup_scraper(weblink, html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        recipe_name = "".join(
             [name.text for name in soup.find_all('h1',
             attrs={'class':'recipe-summary__h1', 'itemprop':'name'})]
            )
        total_reviews = soup.find('span', attrs={'class': 'review-count'}).text
        authors = (
             [" ".join(author.text.split()) for author in
             soup.find_all('h4', attrs={'itemprop': 'author'})]
            )
        ratings = (
             [content['content'] for content in
             soup.find_all('meta', attrs={'itemprop': 'ratingValue'})][1:]
            )
        review_date = (
             [str(date['content']) for date in soup.find_all
             ('meta', attrs={'itemprop': 'dateCreated'})]
            )
        review_data = list(set(zip(authors, ratings, review_date)))
        """ Dump data into mongod """
        collections.insert_one({
            'title': recipe_name,
            'weblink': weblink,
            'total_reviews': total_reviews,
            'review_data': review_data
            })
    except AttributeError:
        pass

    return None


if __name__ == '__main__':
    pickle_list = (['allrecipe_vegetarian_recipelist.pkl'])
    for filename in pickle_list:
        main(filename)
