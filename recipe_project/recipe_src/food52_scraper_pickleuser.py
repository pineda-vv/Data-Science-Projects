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
import pickle

"""
Web scraper to capture recipe ingredients, #likes/votes per recipe name on the
the food52 web site using selenium.  Captured data is stored in a mongodb and
queried subsequently - see recipe_eda.py for methods.
"""

client = MongoClient('mongodb://localhost:27017/')
db = client.food52
food52 = db.food52


def main(filename):
    with open(filename, 'rb') as f:
        link_dict = pickle.load(f)
    link_list = list(link_dict.values())
    recipe_details(link_list)


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


def recipe_details(link_list):
    """
    Opens pages from link list to extract title, rating, recipes
    """
    title_rating = {}
    pages = 0
    for link in link_list:
        num = np.random.randint(3)
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
        print('# recipes')
        print(pages)
        driver.quit()
        if pages / 50 == pages // 50:
            time.sleep(30)
        else:
            continue


def mongo_dump(title, rating, recipe, link):
    food52.insert_one({
        'title': title,
        'rating': rating,
        'recipe': recipe,
        'weblink': link
        })


if __name__ == '__main__':
    ingredients = (
         ['../data/pork.pkl', '../data/beef.pkl',
          '../data/chicken.pkl', '../data/vegetarian.pkl']
        )
    for filename in ingredients:
        main(filename)
