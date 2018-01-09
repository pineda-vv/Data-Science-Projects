import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from time import time

def topic_extraction(df, col_name):
    """
    Two algorithms for topic extraction -
    NMF and LatentDirichletAllocation(LDA).
    Need to tie in with K-means clustering
    """
    rec_stop = (
        ['cup', 'cups', 'tablespoon', 'tablespoons', 'teaspoon', 'teaspoons',
         'pounds', 'ounces', 'grams', 'gram', 'kilograms', 'kilogram', 'liter',
         'liters', 'sliced', 'diced', 'minced', 'finely', 'coarsely',
         'roughly', 'cut', 'peeled', 'chopped']
       )
    my_stop_words = text.ENGLISH_STOP_WORDS.union(rec_stop)
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                       max_features=200,
                                       analyzer='word',
                                       stop_words=my_stop_words)
    tfidf = tfidf_vectorizer.fit_transform(df[col_name])
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                    max_features=200,
                                    stop_words=my_stop_words)
    tf = tf_vectorizer.fit_transform(df[col_name])

    nmf = NMF(n_components=6, random_state=1,
            alpha=.1, l1_ratio=.5)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    nmf_w = nmf.fit_transform(tfidf)
    nmf_h = nmf.components_
    labels = nmf_w.argmax(axis=1)
    df['labels2'] = labels # this was the right code to get labels/clusters
    print("\nTopics in NMF model:")
    print_top_words(nmf, tfidf_feature_names)
    """uncomment to LDA topics"""
    lda = LatentDirichletAllocation(n_components=6, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0,
                                n_jobs=-1)
    mod = lda.fit(tf)
    comp = mod.fit_transform(tf)
    lda_labels = comp.argmax(axis=1)
    df['lda_topics2'] = lda_labels
    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names)
    return df, labels, lda_labels, tfidf, tf


def print_top_words(model, feature_names, n_top_words=20):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print('End')
