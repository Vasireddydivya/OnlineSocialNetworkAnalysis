"""
classify.py
"""

import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn import svm
import os

def read_data(filename,flag):
    twitter_text = []

    with open(filename,'r') as fp:
        csv_read = csv.reader(fp)
        # if flag:


