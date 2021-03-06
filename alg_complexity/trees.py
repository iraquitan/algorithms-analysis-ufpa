# -*- coding: utf-8 -*-
import os
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from random import randint

os.environ['PATH'] += ':/usr/local/bin'
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

warnings.filterwarnings("ignore")


class Node(object):
    def __init__(self, key, left=None, right=None, p=None):
        self.key = key
        self.left = left
        self.right = right
        self.p = p

    def __repr__(self):
        return f"Node[{self.key}]"


class AVLNode(Node):
    def __init__(self, key, left=None, right=None, p=None):
        super(AVLNode, self).__init__(key, left, right, p)
        self.h = 0

    @property
    def is_leaf(self):
        return self.left is None and self.right is None

    def height(self):
        left_h, right_h = 0, 0
        if self is None:
            return -1
        if self.left:
            left_h = self.left.h
        if self.right:
            right_h = self.right.h
        return max(left_h, right_h) + 1

    @property
    def balance_factor(self):
        h_left, h_right = 0, 0
        if self.left:
            h_left = self.left.h
        if self.right:
            h_right = self.right.h
        return h_left - h_right

    def update_height(self):
        self.h = self.height()

    def __repr__(self):
        return f"Node[{self.key}, h={self.h}]"


class AVLNode2(Node):
    def __init__(self, key, left=None, right=None, p=None):
        super(AVLNode2, self).__init__(key, left, right, p)

    @property
    def is_leaf(self):
        return self.left is None and self.right is None

    @property
    def h(self):
        left_h, right_h = 0, 0
        if self is None:
            return -1
        # if self.is_leaf:
        #     return 1
        if self.left:
            left_h = self.left.h
        if self.right:
            right_h = self.right.h
        return max(left_h, right_h) + 1

    @property
    def balance_factor(self):
        h_left, h_right = 0, 0
        if self.left:
            h_left = self.left.h
        if self.right:
            h_right = self.right.h
        return h_left - h_right

    def __repr__(self):
        return f"Node[{self.key}, h={self.h}]"


class RedBlackNode(Node):
    def __init__(self, key, left=None, right=None, p=None, red=True):
        super(RedBlackNode, self).__init__(key, left, right, p)
        self.red = red

    @property
    def color(self):
        return 'red' if self.red else 'black'

    def __repr__(self):
        return f"Node[{self.key}, c={self.color}]"


def node_selector(node_type='Node'):
    NODES = {
        'BinarySearchTree': Node,
        'AVLTree': AVLNode,
        'RedBlackTree': RedBlackNode
    }
    return NODES[node_type]


def nil_selector(nil_type='Node'):
    NILS = {
        'BinarySearchTree': None,
        'AVLTree': None,
        'RedBlackTree': RedBlackNode(None, red=False)
    }
    return NILS[nil_type]


class BaseTree(ABC):

    @abstractmethod
    def __init__(self, keys=None, debug=False):
        self.nil = nil_selector(self.__class__.__name__)
        self.root = self.nil
        self.debug = debug
        if keys is not None:
            self._add_keys(keys)
            # for k in keys:
            #     self.tree_insert(k)

    def _add_keys(self, keys):
        for k in keys:
            self.tree_insert(k)
        # self.root = self.nil

    @abstractmethod
    def tree_insert(self, value):
        if self.debug:
            print(f'Inserting value {value}')
        z = node_selector(self.__class__.__name__)(value)
        self._tree_insert(z)
        return z

    @abstractmethod
    def _tree_insert(self, z):
        pass

    def inorder_tree_walk(self, x):
        if x != self.nil:
            self.inorder_tree_walk(x.left)
            print(x.key)
            self.inorder_tree_walk(x.right)

    def preorder_tree_walk(self, x):
        if x != self.nil:
            print(x.key)
            self.inorder_tree_walk(x.left)
            self.inorder_tree_walk(x.right)

    def postorder_tree_walk(self, x):
        if x != self.nil:
            self.inorder_tree_walk(x.left)
            self.inorder_tree_walk(x.right)
            print(x.key)

    def search(self, key, mode='recursive'):
        if mode == 'recursive':
            return self.tree_search(self.root, key)
        elif mode == 'iterative':
            return self.ite_tree_search(self.root, key)
        else:
            raise ValueError("'mode' must be 'recursive' or 'iterative'")

    def tree_search(self, x, k):
        # if x == self.nil or k == x.key:
        #     return x
        if x == self.nil:
            if self.debug:
                print(f"Key {k} not found.")
            return x
        if k == x.key:
            if self.debug:
                print(f"Key {k} found.")
            return x
        if k < x.key:
            return self.tree_search(x.left, k)
        else:
            return self.tree_search(x.right, k)

    def ite_tree_search(self, x, k):
        while x != self.nil and k != x.key:
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def min(self, x=None):
        if x:
            return self._tree_min(x)
        else:
            return self._tree_min(self.root)

    def _tree_min(self, x):
        while x.left != self.nil:
            x = x.left
        return x

    def max(self, x=None):
        if x:
            return self._tree_max(x)
        else:
            return self._tree_max(self.root)

    def _tree_max(self, x):
        while x.right != self.nil:
            x = x.right
        return x

    def tree_successor(self, x):
        if x.right != self.nil:
            return self.min(x.right)
        y = x.p
        while y != self.nil and x == y.right:
            x = y
            y = y.p
        return y

    def tree_predecessor(self, x):
        raise NotImplemented("TBI")

    @staticmethod
    def _draw_add_node(G, x):
        G.add_node(x.key)

    def _preorder_tree_graph(self, x, G):
        if x != self.nil:
            self._draw_add_node(G, x)
            if x.p != self.nil:
                G.add_edge(x.p.key, x.key)
            self._preorder_tree_graph(x.left, G)
            self._preorder_tree_graph(x.right, G)
        return G

    def draw(self):
        G = nx.DiGraph()
        self._preorder_tree_graph(self.root, G)
        return G

    def plot(self, show=False):
        G = self.draw()
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        pos = graphviz_layout(G, prog='dot')
        nx.draw(G, pos, alpha=0.8, node_color='lightblue', with_labels=True,
                ax=ax)
        ax.axis('equal')
        if show:
            plt.show()
        return fig


class BinarySearchTree(BaseTree):

    def __init__(self, keys=None, debug=False):
        super().__init__(keys, debug)

    def tree_insert(self, value):
        z = super().tree_insert(value)
        return z

    def _tree_insert(self, z):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y == self.nil:
            self.root = z  # Tree was empty
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        return y

    def transplant(self, u, v):
        if u.p == self.nil:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        if v != self.nil:
            v.p = u.p

    def tree_delete(self, value):
        z = self.tree_search(self.root, value)
        if z != self.nil:
            if self.debug:
                print(f"Deleting key {value}.")
            ret = self._tree_delete(z)
            if ret:
                return ret
            else:
                return z.p

    def _tree_delete(self, z):
        if z.left == self.nil:
            self.transplant(z, z.right)
            return z.right
        elif z.right == self.nil:
            self.transplant(z, z.left)
            return z.left
        else:
            y = self.min(z.right)  # Successor of z
            if y.p != z:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.transplant(z, y)
            y.left = z.left
            y.left.p = y
            return y.right

    def left_rotate(self, x):
        y = x.right  # Set y
        if self.debug:
            print(f"\tleft rotating x={x.key}, y={y.key}")
        x.right = y.left  # Turn y's left subtree into x's right subtree
        if y.left != self.nil:
            y.left.p = x
        y.p = x.p  # Link x's parent to y
        if x.p == self.nil:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x  # Put x on y's left
        x.p = y
        return y

    def right_rotate(self, y):
        x = y.left  # Set x
        if self.debug:
            print(f"\tright rotating y={y.key}, x={x.key}")
        y.left = x.right  # Turn x's right subtree into y's left subtree
        if x.right != self.nil:
            x.right.p = y
        x.p = y.p  # Link y's parent to x
        if y.p == self.nil:
            self.root = x
        elif y == y.p.right:
            y.p.right = x
        else:
            y.p.left = x
        x.right = y  # Put y on x's right
        y.p = x
        return x


class AVLTree(BinarySearchTree):

    def tree_insert(self, value):
        z = super().tree_insert(value)
        self.balance(z)

    def left_rotate(self, x):
        y = super().left_rotate(x)
        y.left.update_height()
        y.update_height()
        return y

    def right_rotate(self, y):
        x = super().right_rotate(y)
        x.right.update_height()
        x.update_height()
        return x

    def tree_delete(self, value):
        x = super().tree_delete(value)
        if x:
            self.balance(x)
            return x

    def balance(self, z):
        while z:
            z.update_height()
            bf = z.balance_factor
            if bf <= -2:
                if z.right.balance_factor > 0:
                    self.right_rotate(z.right)
                self.left_rotate(z)
            elif bf >= 2:
                if z.left.balance_factor < 0:
                    self.left_rotate(z.left)
                self.right_rotate(z)
            z = z.p

    def balance2(self, z):
        bf = z.balance_factor
        if abs(bf) <= 1:
            return z
        elif bf < 0:
            if z.right.balance_factor > 0:
                self.right_rotate(z.right)
            return self.left_rotate(z)
        else:
            if z.left.balance_factor < 0:
                self.left_rotate(z.left)
            return self.right_rotate(z)

    def balance3(self, z):
        p = z.p

        bf = z.balance_factor
        if abs(bf) <= 1:
            return z
        elif bf < 0:
            if z.right.balance_factor > 0:
                self.right_rotate(z.right)
            self.left_rotate(z)
        else:
            if z.left.balance_factor < 0:
                self.left_rotate(z.left)
            self.right_rotate(z)
        if p != self.nil:
            self.balance3(p)


class RedBlackTree(BinarySearchTree):

    def __init__(self, keys=None, debug=False):
        super().__init__(keys, debug)
        self.nodes_red = []
        self.nodes_black = []

    def tree_insert(self, value):
        z = super().tree_insert(value)
        self._insert_fixup(z)

    def _tree_insert(self, z):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y == self.nil:
            self.root = z  # Tree was empty
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        return z

    def _insert_fixup(self, z):
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p.red = False
                    y.red = False
                    z.p.p.red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self.left_rotate(z)
                    z.p.red = False
                    z.p.p.red = True
                    self.right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p.red = False
                    y.red = False
                    z.p.p.red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self.right_rotate(z)
                    z.p.red = False
                    z.p.p.red = True
                    self.left_rotate(z.p.p)
        self.root.red = False

    def transplant(self, u, v):
        if u.p == self.nil:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def tree_delete(self, value):
        return super().tree_delete(value)

    def _tree_delete(self, z):
        y = z
        y_orig_color = y.red
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.min(z.right)
            y_orig_color = y.red
            x = y.right
            if y.p == z:
                x.p = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.transplant(z, y)
            y.left = z.left
            y.left.p = y
            y.red = z.red
        if not y_orig_color:  # If y's original color is BLACK
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and not x.red:
            if x == x.p.left:
                w = x.p.right
                if w.red:
                    w.red = False
                    x.p.red = True
                    self.left_rotate(x.p)
                    w = x.p.right
                if not w.left.red and not w.right.red:
                    w.red = True
                    x = x.p
                else:
                    if not w.right.red:
                        w.left.red = False
                        w.red = True
                        self.right_rotate(w)
                        w = x.p.right
                    w.red = x.p.red
                    x.p.red = False
                    w.right.red = False
                    self.left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.red:
                    w.red = False
                    x.p.red = True
                    self.right_rotate(x.p)
                    w = x.p.left
                if not w.right.red and not w.left.red:
                    w.red = True
                    x = x.p
                else:
                    if not w.left.red:
                        w.right.red = False
                        w.red = True
                        self.left_rotate(w)
                        w = x.p.left
                    w.red = x.p.red
                    x.p.red = False
                    w.left.red = False
                    self.right_rotate(x.p)
                    x = self.root
        x.red = False

    def _draw_add_node(self, G, x):
        if x.key is not None:
            G.add_node(x.key, color=x.color, fillcolor=x.color)
            if x.red:
                self.nodes_red.append(x.key)
            else:
                self.nodes_black.append(x.key)

    def _preorder_tree_graph(self, x, G):
        if x != self.nil:
            self._draw_add_node(G, x)
            if x.p != self.nil:
                G.add_edge(x.p.key, x.key)
            self._preorder_tree_graph(x.left, G)
            self._preorder_tree_graph(x.right, G)
        return G

    def plot(self, show=False, save=False):
        G = self.draw()
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        pos = graphviz_layout(G, prog='dot')
        nx.draw_networkx_nodes(G, pos, node_color='k',
                               nodelist=self.nodes_black, alpha=0.8, ax=ax)
        nx.draw_networkx_nodes(G, pos, node_color='r', nodelist=self.nodes_red,
                               alpha=0.8, ax=ax)
        nx.draw_networkx_edges(G, pos, ax=ax)
        nx.draw_networkx_labels(G, pos, font_color='white',
                                nodelist=self.nodes_black, ax=ax)
        ax.axis('equal')
        if show:
            plt.show()
        self.nodes_red = []
        self.nodes_black = []
        return fig


if __name__ == '__main__':
    # keys = [2, 5, 9, 12, 13, 15, 17, 18, 19]
    # keys = [ord(c) for c in 'mnolkqphia']
    n = 60
    keys = list({randint(0, n*4) for x in range(n)})
    # keys = list(range(n))
    # keys.reverse()
    # keys = [10, 6, 15, 3, 7, 17, 2, 4, 5]
    # keys = [10, 20, 30, 5, 3, 50, 40, 70, 60, 90]
    # bst = AVLTree(keys, debug=True)
    bst = RedBlackTree(keys, debug=True)
    fig = bst.plot(show=True)
    # for k in [20, 60, 90]:
    for _ in range(20):
        k = randint(0, len(keys) - 1)
        del_node = bst.tree_delete(keys[k])
    #     del_node = bst.tree_delete(k)
        if del_node:
            bst.plot(show=True)
