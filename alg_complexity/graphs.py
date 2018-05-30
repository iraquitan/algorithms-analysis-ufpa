# -*- coding: utf-8 -*-
import itertools
import networkx as nx
import pandas as pd


def get_shortest_paths_distances(graph, pairs, edge_weight_name):
    """Compute shortest distance between each pair of nodes in a graph.

    Return a dictionary keyed on node pairs (tuples).
    """
    distances = {}
    for pair in pairs:
        distances[pair] = nx.dijkstra_path_length(
            graph, pair[0], pair[1], weight=edge_weight_name
        )
    return distances


def create_complete_graph(pair_weights, flip_weights=True):
    """
    Create a completely connected graph using a list of vertex pairs and the
    shortest path distances between them.

    Parameters:
        pair_weights: list[tuple] from the output of
            get_shortest_paths_distances.
        flip_weights: Boolean. Should we negate the edge attribute in
            pair_weights?
    """
    g = nx.Graph()
    for k, v in pair_weights.items():
        wt_i = -v if flip_weights else v
        g.add_edge(k[0], k[1], attr_dict={"distance": v, "weight": wt_i})
    return g


def add_augmenting_path_to_graph(graph, min_weight_pairs):
    """
    Add the min weight matching edges to the original graph
    Parameters:
        graph: NetworkX graph (original graph from trailmap)
        min_weight_pairs: list[tuples] of node pairs from min weight matching
    Returns:
        augmented NetworkX graph
    """

    # We need to make the augmented graph a MultiGraph so we can add parallel
    # edges
    graph_aug = nx.MultiGraph(graph.copy())
    for pair in min_weight_pairs:
        graph_aug.add_edge(
            pair[0],
            pair[1],
            attr_dict={
                "distance": nx.dijkstra_path_length(graph, pair[0], pair[1]),
                "trail": "augmented",
            },
        )
    return graph_aug


def cpp(G, debug=False):
    odd_nodes = [v for v, d in nx.degree(G) if d % 2 == 1]
    if debug:
        print("Original graph:")
        print(f"\tNumber of nodes = {len(G.number_of_nodes())}")
        print(f"\tNumber of nodes with odd degree = {len(odd_nodes)}")
    odd_nodes_pairs = itertools.combinations(odd_nodes)
    if debug:
        print(f"Number of odd nodes pairs = {len(odd_nodes_pairs)}")
    odd_nodes_pairs_shortest_paths = get_shortest_paths_distances(
        G, odd_nodes, "distance"
    )

    # Generate the complete graph
    g_odd_complete = create_complete_graph(
        odd_nodes_pairs_shortest_paths, flip_weights=True
    )
    if debug:
        print("Complete graph of odd nodes:")
        print(f"\tNumber of nodes: {len(g_odd_complete.nodes())}")
        print(f"\tNumber of edges: {len(g_odd_complete.edges())}")

    # Compute min weight matching
    # Note: max_weight_matching uses the 'weight' attribute by default as the
    # attribute to maximize
    odd_matching_dupes = nx.algorithms.max_weight_matching(g_odd_complete, True)
    if debug:
        print(f"Number of edges in matching: {len(odd_matching_dupes)}")

    # Convert matching to list of deduped tuples
    odd_matching = list(
        pd.unique([tuple(sorted([k, v])) for k, v in odd_matching_dupes.items()])
    )
    if debug:
        print(f"Number of edges in matching (deduped): {len(odd_matching)}")

    # Create augmented graph: add the min weight matching edges to g
    G_aug = add_augmenting_path_to_graph(G, odd_matching)
    if debug:
        print(f"Number of edges in original graph: {len(G.edges())}")
        print(f"Number of edges in augmented graph: {len(G_aug.edges())}")
