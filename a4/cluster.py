"""
FILE DESCRIPTION:
-----------------
This file contains all methods related to graph clustering/community detection , here i used the data collected in
Collector.py , i have collected 300 followers of Ellon Musk and for each of those followers i have collected 300 more
who are following the main follower of Ellon Musk (Basically the direct followers and 1 hop away followers of ellon musk).
Then i am using girvan-newman's clustering technique to identify clusters in the main graph, also i am plotting the
graph before and after clustering occurs.
Here my main aim was to check and see if they were any different communities of users who followed Ellon musk and what
type of community each one of them were.
Module Requirements for this File:
1) Collections
2) Networkx
3) Json
4) matplotlib
5) itertools
6) OS
7) faker
Here faker can be installed through the pip installer using the command -- pip install faker
"""
from faker import Factory
from collections import defaultdict
from networkx import edge_betweenness_centrality as betweeness
import networkx as nx
import json
import matplotlib.pyplot as plt
import itertools
import os

