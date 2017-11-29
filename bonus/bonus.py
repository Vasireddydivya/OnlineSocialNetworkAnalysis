import networkx as nx


def jaccard_wt(graph, node):
    """
    The weighted jaccard score, defined above.
    Args:
      graph....a networkx graph
      node.....a node to score potential new edges for.
    Returns:
      A list of ((node, ni), score) tuples, representing the
                score assigned to edge (node, ni)
                (note the edge order)
    """
    neighbors = set(graph.neighbors(node))
    degree = graph.degree()
    denom_a = 1 / sum(degree[neighbor] for neighbor in neighbors)
    scores = []
    for n in graph.nodes():
        nume = 0
        neighbors2 = set(graph.neighbors(n))
        denom_b = 1 / sum(degree[neighbor] for neighbor in neighbors2)
        common_neighbors = neighbors & neighbors2
        if n not in neighbors and node != n:
            for neigh in common_neighbors:
                nume += 1 / degree[neigh]
            value = nume / (denom_a + denom_b)
            scores.append(((node, n), value))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores