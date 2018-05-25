# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from networkx.drawing.nx_pydot import graphviz_layout

if __name__ == '__main__':
    os.environ['PATH'] += ':/usr/local/bin'

    map = {
        0: r'$\alpha_1$',
        1: r'$\alpha_2$',
        2: r'$\alpha_3$',
        3: '1',
        4: '2',
        5: r'$\beta_1$',
        6: r'$\beta_2$',
        7: r'$\beta_3$',
    }

    dod = {
        'a1': {
            '1': {'weight': 1},
            '2': {'weight': 3}
        },
        'a2': {
            '1': {'weight': 2},
            '2': {'weight': 3}
        },
        'a3': {
            '2': {'weight': 1},
            'b3': {'weight': 4}
        },
        '1': {
            '2': {'weight': 1},
            'b1': {'weight': 2},
            'b2': {'weight': 4}
        },
        '2': {
            'b1': {'weight': 3},
            'b2': {'weight': 5},
            'b3': {'weight': 2}
        },
    }

    adj_mat = np.array([[0, 0, 0, 1, 3, 0, 0, 0],
                        [0, 0, 0, 2, 3, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0, 4],
                        [0, 0, 0, 0, 1, 2, 4, 0],
                        [0, 0, 0, 0, 0, 3, 5, 2],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0]])

    # G = nx.DiGraph(adj_mat)
    G = nx.DiGraph(dod)
    # G = nx.relabel_nodes(G, map)
    # pos = nx.random_layout(G)
    pos = graphviz_layout(G, prog='dot')
    nx.draw(G, pos, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.show()

    print(G)

