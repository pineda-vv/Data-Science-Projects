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
    """
    Scraper for recipe links from main page of allrecipes.com.
    Search items are 'pork', 'chicken', 'beef', 'vegetarian'.
    100 pages of recipes = 5000
    """
    search_links = (
     {'pork': 'http://allrecipes.com/search/results/?wt=pork&sort=re&page=',
      'chicken':'http://allrecipes.com/search/results/?wt=chicken&sort=re&page=',
      'beef': 'http://allrecipes.com/search/results/?wt=beef&sort=re&page=',
      'vegetarian': 'http://allrecipes.com/search/results/?wt=vegetarian&sort=re&page='
     }
    )
    for key, link in search_links.items():
        link_list = []
        for page_num in range(1, 201):
            pause = np.random.randint(3)
            time.sleep(pause)
            link_list += recipe_links(link + str(page_num))
            print(page_num)
        print(key)
        print(len(link_list))
        """
        Saves list of links to a pickle file in case the next step falters.
        Comment out if you just want to do it continuously
        """
        filename_out = '../data/allrecipe_{}_recipelist.pkl'.format(key)
        with open(filename_out, 'wb') as f:
            pickle.dump(link_list, f, pickle.HIGHEST_PROTOCOL)
    """ Sends pickled list to next scraper """
        # recipe_details(filename_out)


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


def recipe_details(filename):
    """
    Opens pages from link list to extract title, rating, recipes
    """
    """ Uncomment if link list is saved as a pickle file """
    with open(filename, 'rb') as f:
        link_list = pickle.load(f)
    pages = 0
    for link in link_list[:2]:
        num = np.random.randint(2) # built in pause
        time.sleep(num)
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=800x841')
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('http:allrecipes.com/recipe' + link)
        try:
            reviewclick = driver.find_element_by_class_name('read--reviews ng-click-active').click()
            selector = driver.find_element_by_css_selector(
            '#ngdialog4-aria-describedby > div > div.review-modal-header > div.tabs > div.selected'
            ).click()
            time.sleep(1)
            rater = driver.find_element_by_class_name('ng-binding')
            rating = driver.find_element_by_class_name('rating')
            review = driver.find_element_by_class_name('ReviewText ng-binding')
            print (rater.text, rating.text, review.text)
        # except (NoSuchElementException, TimeoutException):
            pass

        # except (NoSuchElementException, TimeoutException):
        #     pass
        # mongo_dump(
            #  title.text, rating.text, recipe.text, 'https://food52.com' + link
            # )
        pages += 1
        """
        Counter to keep track of progress - in case it fails at some
        point, can continue from that index on
        """
        print('# recipes')
        print(pages)
        driver.quit()
        if pages / 50 == pages // 50:
            time.sleep(30) # pauses for 30 seconds after 50 scrapes
        else:
            continue


def mongo_dump(title, rating, recipe, link):
    # main()  # uncomment if just starting
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
    pickled_files = (
            ['../data/allrecipe_vegetarian_recipelist.pkl',
             '../data/allrecipe_pork_recipelist.pkl',
             '../data/allrecipe_chicken_recipelist.pkl',
             '../data/allrecipe_beef_recipelist.pkl']
        )
    for filename in pickled_files:
        recipe_details(filename)
