# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 22:53:09 2017
edited
@author: vasir
"""

from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI
import json
from itertools import combinations

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


def read_screen_names(filename):
    """
    Read a text file containing Twitter screen_names, one per line.
    Params:
        filename....Name of the file to read.
    Returns:
        A list of strings, one per screen_name, in the order they are listed
        in the file.
    Here's a doctest to confirm your implementation is correct.
    >>> read_screen_names('candidates.txt')
    ['DrJillStein', 'GovGaryJohnson', 'HillaryClinton', 'realDonaldTrump']
    """
    l = []
    with open(filename) as fh:
        for line in fh:
            line = line.strip()
            l.append(line)
    return l


#    screen_names=open(filename)
#    sn=screen_names.read().split()
#    return sn

def get_users(twitter, screen_names):
    """Retrieve the Twitter user objects for each screen_name.
    Params:
        twitter........The TwitterAPI object.
        screen_names...A list of strings, one per screen_name
    Returns:
        A list of dicts, one per user, containing all the user information
        (e.g., screen_name, id, location, etc)
    See the API documentation here: https://dev.twitter.com/rest/reference/get/users/lookup
    In this example, I test retrieving two users: twitterapi and twitter.
    >>> twitter = get_twitter()
    >>> users = get_users(twitter, ['twitterapi', 'twitter'])
    >>> [u['id'] for u in users]
    [6253282, 783214]
    """
    request = robust_request(twitter, 'users/lookup', {'screen_name': screen_names})
    get_user = []
    for user in request:
        get_user.append(user)
    return get_user
    # for name in screen_names:


def get_friends(twitter, screen_name):
    """ Return a list of Twitter IDs for users that this person follows, up to 5000.
    See https://dev.twitter.com/rest/reference/get/friends/ids
    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.
    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
    Returns:
        A list of ints, one per friend ID, sorted in ascending order.
    Note: If a user follows more than 5000 accounts, we will limit ourselves to
    the first 5000 accounts returned.
    In this test case, I return the first 5 accounts that I follow.
    >>> twitter = get_twitter()
    >>> get_friends(twitter, 'aronwc')[:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    t = robust_request(twitter, 'friends/ids', {'screen_name': screen_name})
    friend_list = []
    for name in t:
        friend_list.append(name)
    return sorted(friend_list)


def add_all_friends(twitter, users):
    """ Get the list of accounts each user follows.
    I.e., call the get_friends method for all 4 candidates.
    Store the result in each user's dict using a new key called 'friends'.
    Args:
        twitter...The TwitterAPI object.
        users.....The list of user dicts.
    Returns:
        Nothing
    >>> twitter = get_twitter()
    >>> users = [{'screen_name': 'aronwc'}]
    >>> add_all_friends(twitter, users)
    >>> users[0]['friends'][:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    for user in users:
        user['friends'] = get_friends(twitter, user['screen_name'])


def print_num_friends(users):
    """Print the number of friends per candidate, sorted by candidate name.
    See Log.txt for an example.
    Args:
        users....The list of user dicts.
    Returns:
        Nothing
    """
    ###TODO
    newlist_users = sorted(users, key=lambda k: k['screen_name'])
    for user in newlist_users:
        print("Number of friends for " + user['screen_name'] + " are: " + str(len(user['friends'])))


def count_friends(users):
    """ Count how often each friend is followed.
    Args:
        users: a list of user dicts
    Returns:
        a Counter object mapping each friend to the number of candidates who follow them.
        Counter documentation: https://docs.python.org/dev/library/collections.html#collections.Counter
    In this example, friend '2' is followed by three different users.
    >>> c = count_friends([{'friends': [1,2]}, {'friends': [2,3]}, {'friends': [2,3]}])
    >>> c.most_common()
    [(2, 3), (3, 2), (1, 1)]
    """
    ###TODO
    #    friend_list=[]
    #    for user in users:
    #        f={'friends':user['friends']}
    #        friend_list.append(f)
    # print(friend_list)
    t = Counter()
    for user in users:
        t.update(user['friends'])
    return t


def friend_overlap(users):
    """
    Compute the number of shared accounts followed by each pair of users.
    Args:
        users...The list of user dicts.
    Return: A list of tuples containing (user1, user2, N), where N is the
        number of accounts that both user1 and user2 follow.  This list should
        be sorted in descending order of N. Ties are broken first by user1's
        screen_name, then by user2's screen_name (sorted in ascending
        alphabetical order). See Python's builtin sorted method.
    In this example, users 'a' and 'c' follow the same 3 accounts:
    >>> friend_overlap([
    ...     {'screen_name': 'a', 'friends': ['1', '2', '3']},
    ...     {'screen_name': 'b', 'friends': ['2', '3', '4']},
    ...     {'screen_name': 'c', 'friends': ['1', '2', '3']},
    ...     ])
    [('a', 'c', 3), ('a', 'b', 2), ('b', 'c', 2)]
    """
    ###TODO

    friends_overlap_list = []
    for user_1, user_2 in combinations(users, 2):
        friends_overlap = overlap_list(user_1['friends'], user_2['friends'])
        friends_overlap_list.append((user_1['screen_name'], user_2['screen_name'], len(friends_overlap)))
    friends_overlap_list = sorted(friends_overlap_list, key=lambda tup: tup[2], reverse=True)
    return friends_overlap_list

def followed_by_hillary_and_donald(users, twitter):
    """
    Find and return the screen_name of the one Twitter user followed by both Hillary
    Clinton and Donald Trump. You will need to use the TwitterAPI to convert
    the Twitter ID to a screen_name. See:
    https://dev.twitter.com/rest/reference/get/users/lookup
    Params:
        users.....The list of user dicts
        twitter...The Twitter API object
    Returns:
        A string containing the single Twitter screen_name of the user
        that is followed by both Hillary Clinton and Donald Trump.
    """
    ###TODO
    hillary_friends_list = get_friends(twitter, 'HillaryClinton')
    trump_friends_list = get_friends(twitter, 'realDonaldTrump')
    overlap_lst = overlap_list(hillary_friends_list, trump_friends_list)
    request = robust_request(twitter, 'users/lookup', {'user_id': overlap_lst})
    handle_request = json.loads(request.text)
    first_elm = handle_request[0]
    return str(first_elm['screen_name'])


def overlap_list(list1, list2):
    a_multiset = Counter(list1)
    b_multiset = Counter(list2)
    return list((a_multiset & b_multiset).elements())


def create_graph(users, friend_counts):
    """ Create a networkx undirected Graph, adding each candidate and friend
        as a node.  Note: while all candidates should be added to the graph,
        only add friends to the graph if they are followed by more than one
        candidate. (This is to reduce clutter.)
        Each candidate in the Graph will be represented by their screen_name,
        while each friend will be represented by their user id.
    Args:
      users...........The list of user dicts.
      friend_counts...The Counter dict mapping each friend to the number of candidates that follow them.
    Returns:
      A networkx Graph
    """
    ###TODO
    graph = nx.Graph()
    for user in users:
        graph.add_node(user['screen_name'])
        for fri in user['friends']:
            if friend_counts[fri] > 1:
                graph.add_edge(fri, user['screen_name'])
    return graph


def draw_network(graph, users, filename):
    """
    Draw the network to a file. Only label the candidate nodes; the friend
    nodes should have no labels (to reduce clutter).
    Methods you'll need include networkx.draw_networkx, plt.figure, and plt.savefig.
    Your figure does not have to look exactly the same as mine, but try to
    make it look presentable.
    """
    ###TODO
    labels1 = {}
    for user in users:
        labels1[user['screen_name']] = user['screen_name']
    plt.figure(figsize=(20, 20))
    nx.draw_networkx(graph, with_labels=True, nodelist=graph.nodes(), edgelist=graph.edges(), labels=labels1,
                     font_color='blue', font_size=8)
    plt.savefig(filename)


def main():
    """ Main method. You should not modify this. """
    twitter = get_twitter()
    screen_names = read_screen_names('C:/Users/vasir/Desktop/candidates.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    # print(get_friends(twitter,'DrJillStein')[:5])
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    print('found %d users with screen_names %s' %
          (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    print('Friends per candidate:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    followed_by_hillary_and_donald(users, twitter)
    print('User followed by Hillary and Donald: %s' % followed_by_hillary_and_donald(users, twitter))
    graph = create_graph(users, friend_counts)
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph, users, 'network.png')
    print('network drawn to network.png')


if __name__ == '__main__':
    main()
