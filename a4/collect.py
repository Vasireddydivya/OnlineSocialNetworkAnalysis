"""
FILE DESCRIPTION:
-----------------

This file contains all methods that are used to collect my raw data for clustering and classification , I use the twitter
streaming api to collect tweets  occurring instantly (I use the term "Trump" to filter and get tweets that are only
related to Donald Trump for my sentiment analysis) and I use my twitter rest api to collect the followers of Ellon musk
and the corresponding followers of each follower of Ellon Musk for my graph Clustering/Community Detection. I cleaned
tweets of any URL using regex before save it to a csv file, to try and improve my classification results.

Module Requirements for this File:
1) csv
2) json
3) TwitterApi
4) sys
5) time
6) re
7) twitter (Streaming api)
8) os
9) pickle
10) zipfile
11) urlopen

You can install the twitter Streaming api by using the command
-- pip install twitter

"""
from TwitterAPI import TwitterAPI
import json
import csv
import sys
import time
import os
import twitter as twitter_streamer
import re
import string
import pickle
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
from collections import defaultdict

consumer_key = 'zvltV4ctBlEO4INU7GTrfvEEr'
consumer_secret = 'FoNAKaCLCYyLtFaSb8mRBpSDV9skd68tXmAgiLf9vFeTZlDaRT'
access_token = '2209159812-IFSHdaseW96iiVj6MABIK7745x8GZQCG262KW9h'
access_token_secret = 'Jm3H7FQlgWEHkTX23iLAKRxnyC80cLgtJHwLKIcH9bQXN'


def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def robust_request(resource, params, max_tries=5):
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
        twitter = get_twitter()
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        elif request.status_code == 401 or request.status_code == 34:
            print('Got error %s %s \nsleeping for 10 seconds.' % (request.text, request.status_code))
            print(params)
            time.sleep(10)
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text )
            sys.stderr.flush()
            time.sleep(61 * 15)


def stream_tweets(search_term, num_tweets=20):
    """ This function uses streaming API to collect tweets that contains given search term.
        This function collects the tweets and then saves into json file.
        Args:
          searchTerm .... The term to search the tweets.
          count ... The number of tweets you want to collect

        Returns:
          Number of tweets collected in a list.
        """
    if not os.path.isfile(os.path.join("Collect_Folder", 'data.txt')):
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
        print("\nCollected " + str(len(tweets_list)) + " using the term " + str(search_term))
    else:
        tweets_list = json.load(open(os.path.join("Collect_Folder", 'data.txt')))
    return len(tweets_list)


def clean_tweet(tweet):
    """
        :param tweet:
        :return:
    """
    line = re.sub(r'[.,@$"!%-&+]+', '', tweet, flags=re.MULTILINE)  # removes the characters specified
    line = re.sub(r'^RT[\s]+', '', line, flags=re.MULTILINE)  # removes RT
    line = re.sub(r'https?:\/\/.*[\r\n]*', '', line, flags=re.MULTILINE)  # remove link
    line = re.sub(r'[:]+', '', line, flags=re.MULTILINE)
    line = list(filter(lambda x: x in string.printable, line))  # filter non-ascii characters
    line = ''.join(l for l in line)
    new_line = ''
    for i in line.split():  # remove @ and #words, punctuataion
        if not i.startswith('@') and not i.startswith('#') and i not in string.punctuation:
            new_line += i + ' '
    line = new_line
    return line


def load_tweets_json_toCsv(filename):
    """
       This  method loads tweets from a file in form of a list of jsons and then creates a dictionary for every tweet.
       From dictionary each tweet is cleaned and writes it to a .csv file for easier processing.(of the form tweet_id,tweet)
       :param      filename: Name of the file to read JSON data from
       :return:    Nothing
    """
    with open("Collect_Folder" + os.path.sep + 'data.txt', 'r') as rp:
        tweet_data = json.load(rp)

    file_name = filename.split('.')[0]
    with open("Collect_Folder" + os.path.sep + file_name + '.csv', 'w') as fp:
        csv_writer = csv.writer(fp, lineterminator="\n")
        # csv_writer.writerow(["ID_str","text"])
        for tweet in tweet_data:
            try:
                cleaned_tweet = clean_tweet(tweet['text'])
                if cleaned_tweet != "":
                    csv_writer.writerow([tweet["id_str"], cleaned_tweet])
            except KeyError:
                pass

    print("\nFinished cleaning tweets and they have been added to data.csv")


def afinn_down():
    url = urlopen('http://www2.compute.dtu.dk/~faan/data/AFINN.zip')
    zipfile = ZipFile(BytesIO(url.read()))
    afinn_file = zipfile.open('AFINN/AFINN-111.txt')
    afinn = dict()
    for line in afinn_file:
        parts = line.strip().split()
        if len(parts) == 2:
            afinn[parts[0].decode("utf-8")] = int(parts[1])
    save_file("Collect_Folder" + os.path.sep + 'afinn_data.txt', afinn)


def save_file(filename, data):
    out = open(filename, 'ab+')
    pickle.dump(data, out)
    out.close()


def label_using_afinn(csv_file, afinn_file):
    result = []
    afinn = pickle.load(open("Collect_Folder" + os.path.sep + afinn_file, 'rb'))

    def tweet_to_rating(tweet):
        return int(sum([afinn[word] for word in tweet.split() if word in afinn]) > 0)

    with open("Collect_Folder" + os.path.sep + csv_file) as fh:
        reader = csv.reader(fh)
        for row in reader:
            row.append(tweet_to_rating(row[1]))
            result.append(row)

    with open("Collect_Folder" + os.path.sep + csv_file.split('.')[0] + "_labeled.csv", 'w') as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["id_str", 'text', 'label'])
        writer.writerows(result)


def get_followers(screen_name, key, count_twt=10):
    """
    Return a list of Twitter IDs for user that this person follows, up to iter.
    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.
    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
        key .......... The key to use in robust_request(screen_name/user_id)
        iter ......... The no of request to fetch
    Returns:
        A set of ints, one per friend ID, sorted in ascending order.
    """
    response = robust_request('followers/ids', {key: screen_name, 'stringify_ids': "true", "count": count_twt})
    followers_ids = {}
    if response != None:
        for follower in response.get_iterator():
            followers_ids[follower] = 0
    return sorted(followers_ids.keys())


def followers_map(screen_name, user_count):
    """
    This method creates a dictionary of user to the list of followers that follow the user. And we write this data to
    the file.
    :param          screen_name : The name of the user who's followers we want
    :param          user_count  : The number of followers you want to get , who follow the user we search for.
    :return:        The no of Users id's we have collected
    """

    # twitter = get_twitter()
    followers = get_followers(screen_name, 'screen_name', user_count)
    followers_dict = {}
    total_users = 0
    followers_dict[screen_name] = followers  # Followers of screen_name
    file_name_followers = os.path.join("Collect_Folder", screen_name + '_followers.pickle')

    if os.path.isfile(file_name_followers):
        fread_followers = open(file_name_followers, 'rb')
        while 1:
            try:
                followers_dict.update(pickle.load(fread_followers))
            except EOFError:
                break
        fread_followers.close()
    print("Numbers of existing followers", len(followers_dict))
    # for loop for adding followers to each follower id
    for index, follower in enumerate(followers):
        if index%15 == 0:
            print("{} followers ".format(index))
        if follower not in followers_dict:
            follow_list = get_followers(follower, 'user_id', user_count)
            with open(file_name_followers, 'ab') as fwrite_followers:
                pickle.dump({follower: follow_list}, fwrite_followers)
            followers_dict[follower] = follow_list

        total_users += len(followers_dict[follower])
    # fwrite_followers.close()
    with open("Collect_Folder" + os.path.sep + screen_name + '.json', 'w') as fp:
        json.dump(followers_dict, fp)
    # fp.close()
    return total_users


def collector_details(No_of_users, No_of_tweets):
    """
    This method saves details of the collection process employed here that is used for tweet and user collection. This
    detail that is saved is later used by Summarize.py
    :param      No_of_users  : The no of user_ids collected that follow ellon musk and ellon musk's followers
    :param      No_of_tweets : The no of tweets collected using the term "trump" for our classification task
    :return:
    """
    with open("Collect_Folder" + os.path.sep + "collector_details.txt", 'w') as fp:
        fp.write("No of Users Collected : " + str(No_of_users) + "\n")
        fp.write("No of tweets Collected : " + str(No_of_tweets) + "\n")

    fp.close()


def main():
    """
        This method executes all the related methods in this file, thereby performing data collection and saving them to
        Collect_Folder.
        :return: Nothing
    """
    print("---------------Collecting data-------------------------------")
    # No_of_tweets = stream_tweets(search_term="Trump", num_tweets=1000)
    # load_tweets_json_toCsv(filename="data.txt")
    # afinn_down()
    # label_using_afinn('data.csv', 'afinn_data.txt')
    No_of_tweets = 1000
    num_users = followers_map(screen_name="elonmusk", user_count=300)
    collector_details(num_users, No_of_tweets)
    print("----------------Finished Collecting----------------------------")


if __name__ == '__main__':
    main()
