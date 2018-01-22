import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import numpy as np
import string
from pymongo import MongoClient
import json
import pickle

"""
Scraper part 2 to extract more data from food52 recipes
"""


def main(filename):
    df = pd.read_csv(filename)
    titles = df['title'].values
    weblinks = df['weblink'].values
    # print(weblinks[:10])
    scraper(titles, weblinks)


def scraper(titles, weblinks):
    count = 0
    dateset = {
         'January', 'February', 'March', 'April', 'May', 'June',
         'July', 'August', 'September', 'October', 'November', 'December'
        }
    for title, link in zip(titles[332:], weblinks[332:]):
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            author = (soup.find('a', attrs={'itemprop': 'author'})).text
            date_test = soup.find(
                 'p', attrs={'class': 'article-header-meta meta'}
                )
            date_string = "".join(
                 [item for item in list(date_test.children)
                  if any(month in item for month in dateset)]
                )
            clean_date = "".join(
                 [" ".join(date_string.split()[idx:idx+3])
                  for idx, item in enumerate(
                  date_string.split()) if item in dateset]
                )
            new_like_count = "".join(
                 list(soup.find('span', attrs={'class': 'counter'}).children)
                )  # to get the count
            serving_search = soup.find('p', attrs={"itemprop": "recipeYield"})
            serves = serving_search.find('strong')
            servings = "".join(
                 [num for num in serves.text.split() if num.isdigit()]
                )
            bb = soup.find_all('div', attrs={'class': 'body'})
            bb_list = [item.text for item in bb if author not in item.text]
        except AttributeError:
            continue
        comments = bb_list[2:]
        count += 1
        """Need to parse this into mongodb dump"""
        # print("Recipe Title {}".format(title))
        # print("Author {}".format(author))
        # print(clean_date)
        # print("Likes {}".format(new_like_count))
        # print(servings)
        # for comment in comments:
        #     print("".join(comment))
        mongo_dump(title, new_like_count, clean_date, servings, comments)
        print(count)
        if count // 25 == count / 25:
            time.sleep(random.randint(20, 30))


def mongo_dump(title, new_rating, date, servings, comments):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.food52_addenda
    data_add = db.new_data
    data_add.insert_one({
        'title': title,
        'rating': new_rating,
        'date_submitted': date,
        'servings': servings,
        'user_comments': comments
        })

if __name__ == '__main__':
    filename = "../data/scraper2_links.csv"
    main(filename)
