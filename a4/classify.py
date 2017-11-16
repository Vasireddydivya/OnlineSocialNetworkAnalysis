"""
FILE DESCRIPTION:
-----------------
This file contains all methods i use to classify my data as having a positive sentiment towards "Donald Trump" or
negative sentiment towards "Trump", Here i have annotated tweets obtained from Collect.py  as 1 or 0
where 1 represents the positive class and 0 represents the negative one. I have annotated labels using Affin dataset.
then using this as my training set i have trained my support vector machine(SVM) classifier using a linear kernel ,
then i collect my tweets at run time and classify the prediction accuracy using the SVM algorithm.
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
from sklearn.svm import SVC
# from sklearn.linear_model import LogisticRegression
import os
import pandas as pd
import numpy as np


def read_data(data_list, flag):
    """
        This method reads the test/train data file and creates a list of test/train data and
        its labels.
        :param      filename: The name of the file to read
        :param      flag    : Stating true if train file or false for test file
        :return:    2 lists, one data list and one label list
        """
    if flag:
        return data_list["text"].tolist(), data_list["label"].tolist()
    else:
        return data_list["text"].tolist()

def vectorize_train_data(data_list, mindf=1, maxdf=1.0):
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


def classify_data(test_vector, train_vector, train_labels,classifier_linear):
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
    classifier_linear.fit(train_vector, train_labels)
    predictions = classifier_linear.predict(test_vector)
    return predictions

# def getClf_GLM():
#     return LogisticRegression(random_state=42)

def getclf_SVM():
    return SVC(kernel='linear')

def accuracy_score(true_labels, predicted_labels):
    """ Compute accuracy of predictions.r
        Params:
          truth labels.......array of true labels (0 or 1)
          predicted labels...array of predicted labels (0 or 1)
        """
    return len(np.where(true_labels == predicted_labels)[0]) / len(true_labels)

def save_classify_details(predicted_labels, X_test):
    """
    This method saves the classification details to classify_details.txt, which will be used in our summary.py
    file to read and display the summary of our classification

    :param    test_data        :  Our list of test tweets obtained from collector.py
    :param    predicted_labels :  Our predicted classes/labels for our test data by our classify method.
    :return:  Nothing
    """
    pos_instance = 0
    neg_instance = 0
    index_pos_instance = 0
    index_neg_instance = 0
    for labl in range(len(predicted_labels)):
        if predicted_labels[labl] == 0:
            index_neg_instance = labl
            neg_instance += 1
        elif predicted_labels[labl] == 1:
            index_pos_instance = labl
            pos_instance += 1
    with open("Classify_Folder"+os.path.sep+'classify_details.txt','w') as fwc:
        fwc.write("Number of positive instances are: " + str(pos_instance) + '\n')
        fwc.write("Positive Instance example is: " + str(X_test[index_pos_instance]) + '\n')
        fwc.write("Number of negative instances are: " + str(neg_instance) + '\n')
        fwc.write("Negative Instance example is: " + str(X_test[index_neg_instance]) + '\n')

def main():
    fields = ['text', 'label']
    twitter_data = pd.read_csv("Collect_Folder" + os.path.sep + "data_labeled.csv", usecols=fields)
    all_data, all_labels = read_data(twitter_data, True)
    all_data_vector, vectorize = vectorize_train_data(data_list=all_data)
    # split all_data into train and test
    X_train, X_test, Y_train,Y_test = train_test_split(all_data_vector,all_labels,test_size=0.35)
    #construct GLM classifier
    # clf_glm = getClf_GLM()
    # predicted_labels = classify_data(X_test, X_train, Y_train,clf_glm)
    # accuracy = accuracy_score(predicted_labels, Y_test)
    # print('Accuracy Score after fitting the GLM classifier on test data is %.4f' % accuracy)
    # save_classify_details(X_test, predicted_labels,'GLM')
    #construct SVM classifier
    clf_svm = getclf_SVM()
    predicted_labels = classify_data(X_test, X_train, Y_train, clf_svm)
    accuracy = accuracy_score(predicted_labels, Y_test)
    print('Accuracy Score after fitting the SVM classifier on test data is %.4f' % accuracy)
    save_classify_details(predicted_labels, all_data)

if __name__ == '__main__':
    main()
