from pymongo import MongoClient
import pandas as pd
import numpy as np

"""
Short method to extract data and remove duplicates from mongodb
One can do this on a Jupyter notebook which is what I did.
"""


def main():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.food52
    food52 = db['food52']
    cursor = food52.find({})
    f52 = [document for document in cursor] # creates list of dicts from mongodb items
    df = pd.DataFrame.from_records(f52)  # create dataframe from list of dicts.
    df['rating'] = df['rating'].apply(to_num)
    df2 = df.copy()
    df2.drop_duplicates(subset='title', inplace=True)
    """ Save data as .csv file """
    df2.to_csv('scraped_data.csv', index=False)


def to_num(col):
    if "," in col:
        a = col.split(",")
        return int("".join(a))
    else:
        return int(col)

if __name__ == '__main__':
    main()
