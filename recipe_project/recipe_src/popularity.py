import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression


def main(filename):
    """
    (EDA) - parse out the scraped data into dataframe
    input = filename
    output = dataframe
    """
    df = pd.read_csv()
    df['ingredient_category'] = df['recipe'].apply(main_ingredient)
    dummies = pd.get_dummies(df['ingredient_category'])
    df2 = concat([df, dummies], axis=1)
    del df2['_id']
    df2.dropna(axis=0, subset=['recipe'], inplace=True)
    df2['label'] = df2['rating'].apply(label)
    """ Top topic extraction -- returns a new dataframe and topic dictionary """
    new_df2, topic_dict = recipe_topic_extraction(df2)
    del new_df2['rating']
    classifier(new_df2, topic_dict)



def main_ingredient(col):
    ingredients = ['pork', 'chicken', 'beef']
    for item in ingredients:
        if item in str(col):
            return item
        else:
            continue

def label(col):
    if col <= 10:
        return True
    if col != 0:
        return False


def recipe_topic_extraction(df):
    """
    topic extraction
    input = dataframe
    output = new_dataframe, topics dictionary (k=topic_number, v=top 5 words)
    """
    title_text = df['title'].values
    tfidf = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    vec_text = tfidf.fit_transform(title_text)
    nmf = NMF(n_components=8, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)
    nmf_w = nmf.fit_transform(tfidf)
    nmf_h = nmf.components_
    df['topics_labels'] = nmf_w.argmax(axis=1)

    df['topic_words'] = df['topic_labels'].apply(lambda x: topics[x])
    dum = pd.get_dummies(df['topics_labels'])
    del dum[7]
    df2 = pd.concat([df, dum], axis=1)
    return df2, topics


def print_top_words(model, feature_names, n_top_words):
    topics = {}
    for topic_idx, topic in enumerate(model.components_):
        # message = "Topic #%d: " % topic_idx
        # message += " ".join([feature_names[i]
        #                      for i in topic.argsort()[:-n_top_words - 1:-1]])
        topics[topic_idx] = " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
    return topics

def classifier(df):
    """
    input - dataframe
    output - classifier model and cross-validation metrics
    """
    y = df.pop('label')
    X = df.values
    X_train, X_test, y_train, y_test = (
         train_test_split(X, y, test_size=0.33, random_state=42)
        )
    gbc = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_features="auto")
    logistic = LogisticRegression(n_jobs=-1)
    mod4 = gbc.fit(X_train, y_train)
    mod3 = logistic.fit(X_train, y_train)


if __name__ == '__main__':
    filename = '../data/food52_scraped_data.csv'
    main(filename)
