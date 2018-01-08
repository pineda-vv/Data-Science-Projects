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


def main(filename, used_links):
    """
    Open pickled list file for recipes and passes each link to the scraper
    """
    with open(filename, 'rb') as f:
        link_list1 = pickle.load(f)
    counter = 0
    links = set(["http://allrecipes.com" + link for link in link_list1])
    link_list = list(links - used_links)
    for link in link_list:
        if 'video' not in link:
            weblink = "http://allrecipes.com" + link

            if weblink not in used_links:
                scraper(weblink)
            else:
                continue
        counter += 1
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
    # assert 'allrecipes' in driver.title, 'Not opening webpage'
    tester = False
    try:
        clicker = driver.find_element_by_css_selector(
             '#reviews > div.recipe-reviews__more-container > div.more-button'
            )
        tester = True
    except (NoSuchElementException, TimeoutException, ElementNotVisibleException, WebDriverException):
        print('No More button')

    if tester:
        for n in range(10):
            try:
                clicker = driver.find_element_by_css_selector(
                     '#reviews > div.recipe-reviews__more-container > div.more-button'
                    )
                clicker.location_once_scrolled_into_view
                clicker.click()
                time.sleep(1)
            except (ElementNotVisibleException, TimeoutException):
                break

        html = driver.page_source
        soup_scraper(weblink, html)
        driver.quit()
    else:
        html = driver.page_source
        soup_scraper(weblink, html)
        driver.quit()

def soup_scraper(weblink, html):
    soup = BeautifulSoup(html, 'html.parser')
    review_totals = 0
    try:
        recipe_name = "".join(
             [name.text for name in soup.find_all('h1',
             attrs={'class':'recipe-summary__h1', 'itemprop':'name'})]
            )
        total_reviews = soup.find('span', attrs={'class': 'review-count'}).text
        review_totals = int(total_reviews.split()[0])
    except AttributeError:
        print('Cannot find title/total reviews')


    if review_totals != 0:
        try:
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
            print(recipe_name)
            """ Dump data into mongod """
            collections.insert_one({
                'title': recipe_name,
                'weblink': weblink,
                'total_reviews': total_reviews,
                'review_data': review_data
                })
        except AttributeError:
            pass
    else:
        print(recipe_name)
        review_data = [None]
        collections.insert_one({
        'title': recipe_name,
        'weblink': weblink,
        'total_reviews': 0,
        'review_data': review_data
        })
    return None

if __name__ == '__main__':
    with open('used_links.pkl', 'rb') as f1:
        used_links = set(pickle.load(f1))
    pickle_list = (['allrecipe_vegetarian_recipelist.pkl'])
    for filename in pickle_list:
        main(filename, used_links)
