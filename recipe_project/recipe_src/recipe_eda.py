from pymongo import MongoClient
import pandas as pd
import numpy as np

client = MongoClient('mongodb://localhost:27017/')
db = client.food52
food52 = db['food52']

cursor = food52.find({})
f52 = [document for document in cursor] # creates list of dicts from mongodb items
df = pd.DataFrame.from_records(f52)  # create dataframe from list of dicts.
def to_num(col):
    if "," in col:
        a = col.split(",")
        return int("".join(a))
    else:
        return int(col)
df['rating'] = df['rating'].apply(to_num)
