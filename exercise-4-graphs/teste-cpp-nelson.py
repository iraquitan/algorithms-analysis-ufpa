import numpy as np
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
from alg_complexity.graphs import cpp  #, animate_circuit, make_circuit_video
import glob
import numpy as np
import copy
import imageio
import os


def create_cpp_edgelist(euler_circuit):
    """
    Create the edgelist without parallel edge for the visualization
    Combine duplicate edges and keep track of their sequence and # of walks
    Parameters:
        euler_circuit: list[tuple] from create_eulerian_circuit
    """
    cpp_edgelist = {}

    for i, e in enumerate(euler_circuit):
        edge = frozenset([e[0], e[1]])

        if edge in cpp_edgelist:
            cpp_edgelist[edge][2]['sequence'] += ', ' + str(i)
            cpp_edgelist[edge][2]['visits'] += 1

        else:
            cpp_edgelist[edge] = e
            cpp_edgelist[edge][2]['sequence'] = str(i)
            cpp_edgelist[edge][2]['visits'] = 1

    return list(cpp_edgelist.values())


def animate_circuit(euler_circuit):
    visit_colors = {1:'black', 2:'red'}
    edge_cnter = {}
    g_i_edge_colors = []

    cpp_edgelist = create_cpp_edgelist(euler_circuit)
    # Create CPP solution graph
    g_cpp = nx.Graph(cpp_edgelist)
    node_positions = graphviz_layout(g_cpp, prog="dot")

    for i, e in enumerate(euler_circuit, start=1):

        edge = frozenset([e[0], e[1]])
        if edge in edge_cnter:
            edge_cnter[edge] += 1
        else:
            edge_cnter[edge] = 1

        # Full graph (faded in background)
        nx.draw_networkx(g_cpp, pos=node_positions, node_size=6, node_color='gray', with_labels=False, alpha=0.07)

        # Edges walked as of iteration i
        euler_circuit_i = copy.deepcopy(euler_circuit[0:i])
        for i in range(len(euler_circuit_i)):
            edge_i = frozenset([euler_circuit_i[i][0], euler_circuit_i[i][1]])
            euler_circuit_i[i][2]['visits_i'] = edge_cnter[edge_i]
        g_i = nx.Graph(euler_circuit_i)
        # g_i_edge_colors = [visit_colors[e[2]['visits_i']] for e in g_i.edges(data=True)]

        g_i_edge_colors = []
        for e in g_i.edges(data=True):
            if e[2].get('visits_i', None) == None:
                continue
            else:
                color = visit_colors[e[2]['visits_i']]
            g_i_edge_colors.append(color)

        nx.draw_networkx_nodes(g_i, pos=node_positions, node_size=6, alpha=0.6, node_color='lightgray', with_labels=False, linewidths=0.1)
        nx.draw_networkx_edges(g_i, pos=node_positions, edge_color=g_i_edge_colors, alpha=0.8)

        plt.axis('off')
        plt.savefig('fig/png/img{}.png'.format(i), dpi=120, bbox_inches='tight')
        plt.close()


def make_circuit_video(image_path, movie_filename, fps=5):
    # sorting filenames in order
    filenames = glob.glob(image_path + 'img*.png')
    filenames_sort_indices = np.argsort([int(os.path.basename(filename).split('.')[0][3:]) for filename in filenames])
    filenames = [filenames[i] for i in filenames_sort_indices]

    # make movie
    with imageio.get_writer(movie_filename, mode='I', fps=fps) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)


if __name__ == '__main__':
    """
    Algoritmo Hungaro ou de Fluxo
    """
    # dod = {
    #     "A": {"B": {"weight": 1}, "C": {"weight": 2}, "D": {"weight": 3}},
    #     "B": {"A": {"weight": 1}, "2": {"weight": 3}},
    #     "C": {"2": {"weight": 1}, "b3": {"weight": 4}},
    #     "D": {"2": {"weight": 1}, "b1": {"weight": 2}, "b2": {"weight": 4}},
    #     "E": {"b1": {"weight": 3}, "b2": {"weight": 5}, "b3": {"weight": 2}},
    # }
    map = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E"
    }
    adj_mat = np.array(
        [
            [0, 1, 2, 3, 4],
            [1, 0, 8, 0, 6],
            [2, 8, 0, 7, 0],
            [3, 0, 7, 0, 5],
            [4, 6, 0, 5, 0],
        ]
    )
    G = nx.Graph(adj_mat)
    G = nx.relabel_nodes(G, map)
    # pos = graphviz_layout(G, prog="dot")
    # nx.draw(G, pos, node_color="lightblue")
    # nx.draw_networkx_edge_labels(G, pos)
    # nx.draw_networkx_labels(G, pos)
    # plt.show()
    path = cpp(G, source="A", debug=True)
    s = 0
    for a, b, w in path:
        # print(f"{a} -> {b}")
        s += w["weight"]
    print(f"soma={s}")
    animate_circuit(path)
    make_circuit_video('fig/png/', 'cpp_anim.gif', fps=3)
