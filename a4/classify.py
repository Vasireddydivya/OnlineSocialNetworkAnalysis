"""
classify.py
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn import svm
import os
import pandas as pd
import numpy as np


def train_test_split(file_name):
    fields = ['text', 'label']
    twitter_data = pd.read_csv("Collect_Folder" + os.path.sep + file_name, usecols=fields)
    test = set(range(len(twitter_data))[::350])
    train = sorted(set(range(len(twitter_data))) - test)
    test = sorted(test)
    return twitter_data.iloc[train], twitter_data.iloc[test]

def read_data(data_list, flag):
    text = []
    label = []
    for row in data_list.iterrows():
        if flag:
            text.append(row[0])
            label.append(row[1])
        else:
            text.append(row[0])
    if flag:
        return text, label
    else:
        return text


def vectorize_train_data(data_list, mindf=4, maxdf=0.8):
    stopword_list = stopwords.words('english')
    vectorizer = TfidfVectorizer(min_df=mindf, max_df=maxdf, sublinear_tf=True, use_idf=True, stop_words=stopword_list)
    data_vector = vectorizer.fit_transform(data_list)
    return data_vector, vectorizer


def vectorize_test_data(test_data_list, vectorizer):
    data_vector = vectorizer.fit_transform(test_data_list)
    return data_vector

def classify_data(test_vector,train_vector,train_labels,strategy='linear'):
    classifier_linear = svm.SVC(kernel=strategy)
    classifier_linear.fit(train_vector,train_labels)
    predictions = classifier_linear.predict(test_vector)
    return predictions

def accuracy_score(true_labels, predicted_labels):
    """ Compute accuracy of predictions.
        Params:
          truth labels.......array of true labels (0 or 1)
          predicted labels...array of predicted labels (0 or 1)
        """
    return len(np.where(true_labels == predicted_labels)[0]) / len(true_labels)

def main():
    tweets_train, tweets_test = train_test_split("data_labeled.csv")
    train_data, train_labels = read_data(tweets_train,True)
    test_data = read_data(tweets_test,False)
    train_vector, vectorize = vectorize_train_data(data_list=train_data)
    test_vector = vectorize_test_data(test_data_list=test_data, vectorizer=vectorize)
    predicted_labels = classify_data(test_vector, train_vector, train_labels)
    accuracy = accuracy_score(predicted_labels,tweets_test['label'])
    print('Accuracy Score after fitting the SVM classifier on test data is %.4f' %accuracy)

if __name__ == '__main__':
    main()