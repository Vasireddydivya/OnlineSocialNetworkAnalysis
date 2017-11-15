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


def create_graph(filename):
    G = nx.Graph()
    with open(filename, 'r') as fp:
        followers_dict = json.load(fp)
    new_dict = dict({key: value for key, value in followers_dict.items() if key != 'elonmusk'})
    G.add_nodes_from(new_dict.keys())
    for key in new_dict:
        for follower in new_dict[key]:
            if follower not in G:
                G.add_node(follower)
                G.add_edge(key, follower)
            elif follower in G and G.has_edge(key, follower) == False and G.has_edge(follower, key) == False:
                G.add_edge(key, follower)
    print("\nCreated graph from data in file --> " + filename + "\n")
    print("\nGraph Contains : ")
    print("----------------")
    print("\n " + str(len(G.nodes())) + " Nodes")
    print("\n " + str(len(G.edges())) + " Edges")
    return G


def save_graph(G):
    """
    This creates an image of our original graph that has not undergone clustering .
    :param      G: Our networkx graph object
    :return:    Nothing
    """
    pos = nx.spring_layout(G, scale=2)
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, alpha=0.5, node_color='r', node_size=20)
    nx.draw_networkx_edges(G, pos, width=0.4, alpha=0.5)
    plt.savefig("Cluster_Folder"+os.path.sep+"Graph.png", dpi=300)  # save as png


def main():
    """
    This method runs the methods defined in this file and saves the details after identifying the clusters and generates
    a graph before clustering and after clustering.
    :return: Nothing
    """

    print("\t\t************************ - Starting cluster.py - ************************ ")

    G = create_graph(filename="Collect_Folder" + os.path.sep + "elonmusk.json")
    save_graph(G)

if __name__ == '__main__':
    main()
