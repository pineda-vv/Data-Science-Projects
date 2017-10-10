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
Web scraper to capture recipe list using the following search terms on
the food52 website front page.  Except for pork, 200 pages worth of recipe
weblinks will be scraped and each list is saved as a pickle file
"""


def main():
    main_ingredient = {
         'pork': 'pork.pkl', 'chicken': 'chicken.pkl',
         'beef': 'beef.pkl', 'vegetarian': 'vegetarian.pkl'
        }
    link = 'https://food52.com/recipes/search?page='
    for key in main_ingredient.keys():
        if key == 'pork':
            page_limit = 66
        else:
            page_limit = 200
        link_list = []
        for page_num in range(1, page_limit):
            pause = np.random.randint(3)
            time.sleep(pause)
            link_list += recipe_links(link + str(page_num) + "&q=" + key)
            print(page_num)
        d = {num: link for num, link in enumerate(link_list)}
        obj = pickle.dumps(d)
        filename = main_ingredient[key]
        with open(filename, 'wb') as f:
            pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)


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


if __name__ == "__main__":
    main()
