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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import numpy as np
import string
import pandas as pd
from collections import defaultdict
from pymongo import MongoClient
import json
import pickle

"""
Web scraper to capture recipe list and number of votes for different recipes on
the food52 web site.  Had to set up ec2 instance to do this.
Don't know what to do with it yet.
"""


def main():
    link_list = []
    link = 'https://food52.com/recipes?page='  # there are 195 pages
    for page_num in range(1, 196):
        pause = np.random.randint(3)
        time.sleep(pause)
        link_list += recipe_links(link + str(page_num))
        print(page_num)
    d = {num: link for num, link in enumerate(link_list)}
    """
    Saves list of links to a pickle file in case the next step falters.
    Comment out if you just want to do it continuously
    """
    with open('festured_link_list.pkl', 'wb') as f:
        pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)
    """ Sends pickled dictionary to next scraper """
    recipe_details(d)


def recipe_links(weblink):
    r = requests.get(weblink)
    soup = BeautifulSoup(r.content, 'html.parser')
    recipes = []
    for link in soup.find_all('a'):
        rec = link.get('href')
        try:
            if rec.startswith('/recipe') and rec[9:11].isdigit():
                recipes.append(rec)
        except AttributeError:
            pass
    return list(set(recipes))


def recipe_details(pickled_dict):
    """
    Opens pages from link list to extract title, rating, recipes
    """
    """ Uncomment if link list is saved as a pickle file """
    # with open(filename, 'rb') as f:
    #     link_dict = pickle.load(f)
    link_dict = pickle.load(pickled_dict)
    link_list = list(link_dict.values())
    recipe_details(link_list)
    pages = 0
    for link in link_list:
        num = np.random.randint(3)  # built in pause
        time.sleep(num)
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=800x841')
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('https://food52.com' + link)
        try:
            title = driver.find_element_by_class_name('article-header-title')
            rating = driver.find_element_by_class_name('counter')
            recipe = driver.find_element_by_class_name('recipe-list')
        except (NoSuchElementException, TimeoutException):
            pass
        mongo_dump(
             title.text, rating.text, recipe.text, 'https://food52.com' + link
            )
        pages += 1
        """
        Counter to keep track of progress - in case it fails at some
        point, can continue from that index on
        """
        print('# recipes')
        print(pages)
        driver.quit()
        if pages / 50 == pages // 50:
            time.sleep(30)  # pauses for 30 seconds after 50 scrapes
        else:
            continue


def mongo_dump(title, rating, recipe, link):
    """ Dump scraped data into mongodb as it comes in """
    client = MongoClient('mongodb://localhost:27017/')
    db = client.food52
    food52 = db.food52
    food52.insert_one({
        'title': title,
        'rating': rating,
        'recipe': recipe,
        'weblink': link
        })

if __name__ == '__main__':
    main()
