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
from networkx import edge_betweenness_centrality as betweenness
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
    new_dict = dict({key: value for key, value in new_dict.items() if value != []})
    G.add_nodes_from(new_dict.keys())
    for key in new_dict:
        for x in new_dict[key]:
            if x not in G:
                G.add_node(x)
                G.add_edge(key, x)
            elif x in G and G.has_edge(key, x) == False and G.has_edge(x, key) == False:
                G.add_edge(key, x)
    print("\nCreated graph from data in file: " + filename + "\n")
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
    pos = nx.spring_layout(G,scale=8)
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, alpha=0.5, node_size=20, node_color='red')
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=0.4)
    plt.savefig("Cluster_Folder" + os.path.sep + "Graph.png", dpi=300)  # save as png


def cluster_graph(G, k):
    """
    This method clusters our given networkx graph into k clusters / communities using girvan_newman algorithm.
    :param      G: Our networkx graph made from twitter data
    :return:    The clusters of our graph.
    """
    comp = girvan_newman(G)
    # print(tuple(sorted(c) for c in next(comp)))
    result = tuple
    for comp in itertools.islice(comp, k - 1):
        result = tuple(sorted(c) for c in comp)
    return result


# The girvan_newman, _without_most_central_edges, most_central_edge copied from the networkX documentation
# https://pastebin.com/ieFfnyy1 - Resource for coping the below 3 functions.
def girvan_newman(G, most_valuable_edge=None):
    """
    This is the code given on the NetworkX Documentation site to implement girvan_Newman.
    :param  G: Our networkx graph object
    :param  most_valuable_edge: The most valuable edge in our graph ( can be based on weight, centrality measure
                                      or betweenness score).
    :return: A generator of communities.
    """
    if G.number_of_edges() == 0:
        yield tuple(nx.connected_components(G))
        return
    if most_valuable_edge is None:
        def most_valuable_edge(G):
            """Returns the edge with the highest betweenness centrality
               in the graph `G`.
            """
            # We have guaranteed that the graph is non-empty, so this
            # dictionary will never be empty.
            betweenness = nx.edge_betweenness_centrality(G)
            return max(betweenness, key=betweenness.get)
    # The copy of G here must include the edge weight data.

    g = G.copy().to_undirected()
    # Self-loops must be removed because their removal has no effect on
    # the connected components of the graph.
    g.remove_edges_from(g.selfloop_edges())
    while g.number_of_edges() > 0:
        yield _without_most_central_edges(g, most_valuable_edge)


def _without_most_central_edges(G, most_valuable_edge):
    """
    Built-in method used for Girvan Newman
    :param G:
    :param most_valuable_edge:
    :return:
    """
    original_num_components = nx.number_connected_components(G)
    num_new_components = original_num_components
    new_components = tuple()
    while num_new_components <= original_num_components:
        edge = most_valuable_edge(G)
        G.remove_edge(*edge)
        new_components = tuple(nx.connected_components(G))
        num_new_components = len(new_components)
    return new_components


def most_central_edge(G):
    """
    Built-in method used for Girvan Newman
    :param G:
    :return:
    """
    centrality = betweenness(G)
    return max(centrality, key=centrality.get)


def save_cluster(cluster_tuple):
    """
    This method saves the clusters of the graph to clusters.txt
    :param          cluster_tuple : The tuple containing the different clusters
    :return:        Nothing
    """
    with open("Cluster_Folder" + os.path.sep + 'cluster.txt', 'w') as fw:
        for tup in range(len(cluster_tuple)):
            fw.write("Cluster " + str(tup) + str(cluster_tuple[tup]) + '\n')

    print("\nClusters are saved to --> " + "cluster.txt in Cluster_Folder folder\n")


def cluster_details(community_tuple):
    """
    This saves the details of the clusters found and saves it to the cluster_details.txt file in the Clusters_Folder
    :param      Communities_tuple: The tuple that contains the clusters of the networkx graph
    :return:    returns dictionary created from community_tuple
    """
    cluster_dict = defaultdict(list)
    for tup in range(len(community_tuple)):
        cluster_dict[tup] = community_tuple[tup]
    # Finding the total communities and number of users per community
    len_dict = len(cluster_dict)
    total_sum = 0.0
    for key in cluster_dict:
        total_sum += len(cluster_dict[key])
    average = total_sum / len_dict
    with open("Cluster_Folder" + os.path.sep + 'cluster_details.txt', 'w') as fwc:
        fwc.write("Number of communities discovered: " + str(len_dict) + '\n')
        fwc.write("Average Number of users per community: " + str(average) + '\n')
    return cluster_dict


def color_creation(num_communities):
    """
    This method creates random colour for each community using the faker python library equal to no of
    clusters/communities found
    :param          no_of_communities: The
    :return:        List of colours equal to no of communities found.
    """
    lst_color = []
    fake = Factory.create()
    for tup in range(num_communities):
        lst_color.append(fake.hex_color())
    return lst_color


def save_clustered_graph(G, clust_dict, color_lst):
    """
    This method creates a graph image using the cluster details and a random list of colours in hexadecimal format that
    is equal to the no of clusters found by girvan-newman.
    :param              G               : The networkx graph object
    :param              com_dict        : The dict containing different communities/clusters
    :param              color_list      : The list containing random hexadecimal notations of colors based
                                          on the number of clusters found
    :return:            Nothing
    """
    node_color = []
    new_graph = G.copy()
    for n in new_graph.nodes():
        for key in clust_dict:
            if n in clust_dict[key]:
                node_color.append(color_lst[key])
    plt.clf()
    pos = nx.spring_layout(new_graph, scale=8)
    plt.axis("off")
    nx.draw_networkx_nodes(new_graph, pos, alpha=0.4, node_size=20, node_color=node_color)
    nx.draw_networkx_edges(new_graph, pos, alpha=0.3, width=0.4)
    plt.savefig("Cluster_Folder" + os.path.sep + "clusteredGraph.png", dpi=300)

def main():
    """
    This method runs the methods defined in this file and saves the details after identifying the clusters and generates
    a graph before clustering and after clustering.
    :return: Nothing
    """

    print("\t\t************************ - Starting cluster.py - ************************ ")

    G = create_graph(filename="Collect_Folder" + os.path.sep + "elonmusk.json")
    save_graph(G)
    result_cluster_tuple = cluster_graph(G=G, k=5)
    save_cluster(result_cluster_tuple)
    community_tuple = cluster_details(result_cluster_tuple)
    colors_lst = color_creation(len(community_tuple))
    save_clustered_graph(G, community_tuple, colors_lst)


if __name__ == '__main__':
    main()
