"""
collect.py
"""
"""
This file contains methods that are needed to collect data and use that raw data for classification and clustering. I use twitter API to collect
tweets.
"""
from TwitterAPI import TwitterAPI
from collections import Counter
import json
import csv
import sys
import time
import os
import twitter as twitter_streamer
import re
import string

consumer_key = 'SnaRKwvH4NOLJmdJOWdTPgIn5'
consumer_secret = 'o3iVzZY0jfLNvDO8A3Q2lRRfniKhyNIwx95HkYp5ye8p2MgPiq'
access_token = '2209159812-IFSHdaseW96iiVj6MABIK7745x8GZQCG262KW9h'
access_token_secret = 'Jm3H7FQlgWEHkTX23iLAKRxnyC80cLgtJHwLKIcH9bQXN'


def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def stream_tweets(search_term, num_tweets=20):
    """ This function uses streaming API to collect tweets that contains given search term.
    This function cleans the tweets that are collected and then saves into .csv file.
        Args:
          searchTerm .... The term to search the tweets.
          count ... The number of tweets you want to collect

        Returns:
          Number of tweets collected in a list.
        """
    tweets_list = []
    # create twitter API object
    oauth = twitter_streamer.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
    stream = twitter_streamer.TwitterStream(auth=oauth, secure=True)
    # iterate over tweets matching this filter text
    tweet_iter = stream.statuses.filter(track=search_term, language='en', retweeted=False)
    with open("Collect_Folder" + os.path.sep + 'data.txt', 'w') as f:
        for tweet in tweet_iter:
            if "text" in tweet:
                text = tweet['text']
                if text.strip().startswith('RT') == False:
                    tweets_list.append(tweet)
            if len(tweets_list) == num_tweets:
                break
        json.dump(tweets_list, f)
    f.close()
    return len(tweets_list)


def clean_tweet(tweet):
    """
        :param tweet:
        :return:
    """
    line = re.sub(r'[.,"!]+', '', tweet, flags=re.MULTILINE)  # removes the characters specified
    line = re.sub(r'^RT[\s]+', '', line, flags=re.MULTILINE)  # removes RT
    line = re.sub(r'https?:\/\/.*[\r\n]*', '', line, flags=re.MULTILINE)  # remove link
    line = re.sub(r'[:]+', '', line, flags=re.MULTILINE)
    line = filter(lambda x: x in string.printable, line)  # filter non-ascii characers

    new_line = ''
    for i in line.split():  # remove @ and #words, punctuataion
        if not i.startswith('@') and not i.startswith('#') and i not in string.punctuation:
            new_line += i + ' '
    line = new_line


def load_tweets_json_toCsv(filename):
    """
       This  method loads tweets from a file in form of a list of jsons and then creates a dictionary for every tweet.
       From dictionary each tweet is cleaned and writes it to a .csv file for easier processing.(of the form tweet_id,tweet)
       :param      filename: Name of the file to read JSON data from
       :return:    Nothing
    """
    with open("Collect_Folder" + os.path.sep + 'data.txt', 'r') as rp:
        tweet_data = json.load(rp)
    rp.close()
    file_name = filename.split('.')[0]
    with open("Collect_Folder" + os.path.sep + file_name + '.csv', 'w') as fp:
        csv_writer = csv.writer(fp)
        for tweet in tweet_data:
            if "id_str" in tweet and "text" in tweet:
                cleaned_tweet = clean_tweet(tweet['text'])
                csv_writer.writerow(tweet["id_str"], cleaned_tweet)
    fp.close()

def main():
    """
        This method executes all the related methods in this file, thereby performing data collection and saving them to
        Collect_Folder.
        :return: Nothing
    """
    print("---------------Collecting data-------------------------------")
    No_of_tweets = stream_tweets(search_term="Trump", num_tweets=1000)
    load_tweets_json_toCsv(filename="data.txt")

    print("----------------Finished Collecting----------------------------")

if __name__ == '__main__':
    main()