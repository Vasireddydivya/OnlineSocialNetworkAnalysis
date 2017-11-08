"""
FILE DESCRIPTION:
-----------------
This file contains all methods i use to classify my data as having a positive sentiment towards "Donald Trump" or
negative sentiment towards "Trump", Here i have annotated tweets obtained from Collect.py  as 1 or 0
where 1 represents the positive class and 0 represents the negative one. I have annotated labels using Affin dataset.
then using this as my training set i have
trained my support vector machine(SVM) classifier using a linear kernel , then i collect my tweets at run time and
i classify them using my trained SVM.
Module Requirements for this File:

1) sklearn
2) nltk
3) os
4) pandas
Here you might need to download the nltk stopwords corpus using the command
-- nltk download , then select the one mentioned as stopwords corpus and download it.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn import svm
import os
import pandas as pd
import numpy as np


def train_test_split(file_name):
    """
    This function reads the CSV file name in Collect_Folder. I'm splitting the data into train and test in 65%, 35%
    respectively. The file is .csv file in the form of (tweet_id,tweet_text,tweet_label).
    :param file_name: The name of the file to read
    :return:
    """
    fields = ['text', 'label']
    twitter_data = pd.read_csv("Collect_Folder" + os.path.sep + file_name, usecols=fields)
    test = set(range(len(twitter_data))[::350])
    train = sorted(set(range(len(twitter_data))) - test)
    test = sorted(test)
    return twitter_data.iloc[train], twitter_data.iloc[test]

def read_data(data_list, flag):
    """
        This method reads the test/train data file and creates a list of test/train data and
        its labels.
        :param      filename: The name of the file to read
        :param      flag    : Stating true if train file or false for test file
        :return:    2 lists, one data list and one label list
        """
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
    """
        This method reads the list of tweets then converts it to a csr_matrix using sklearns built-in function
        we also remove the stopwords from every tweet using nltk's list of stopwords
        :param data_list: list of tweets
        :return: csr_matrix containing tf-idf values of the tweets
        """
    stopword_list = stopwords.words('english')
    vectorizer = TfidfVectorizer(min_df=mindf, max_df=maxdf, sublinear_tf=True, use_idf=True, stop_words=stopword_list)
    data_vector = vectorizer.fit_transform(data_list)
    return data_vector, vectorizer


def vectorize_test_data(test_data_list, vectorizer):
    """
        :param test_data_list:
        :param vectorizer:
        :return:
        """
    data_vector = vectorizer.fit_transform(test_data_list)
    return data_vector

def classify_data(test_vector,train_vector,train_labels,strategy='linear'):
    """
        This method takes in the train and test vectors containing tf-idf scores , train_labels and performs classification
        using SVM(Support Vector Machine, and uses a linear kernel for the strategy) and returns a list of predicted labels
        for the test data.
        :param      test_vector : csr matrix containing tf-idf scores for the test_data
        :param      train_vector: csr matrix containing tf-idf scores for the train_data
        :param      train_labels: list of corresponding labels for the train_data_vector
        :param      strategy    : The type of Kernel to use for a Support Vector Machine
        :return:  A list of predicted labels for the test data
        """
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