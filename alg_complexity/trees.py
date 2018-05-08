# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout


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

    def __repr__(self):
        return f"Node[{self.key}, h={self.h}]"


class BaseTree(object):

    # def __repr__(self):
    #     return self.inorder_tree_walk(self.root)

    def inorder_tree_walk(self, x):
        if x is not None:
            self.inorder_tree_walk(x.left)
            print(x.key)
            self.inorder_tree_walk(x.right)

    def preorder_tree_walk(self, x):
        if x is not None:
            print(x.key)
            self.inorder_tree_walk(x.left)
            self.inorder_tree_walk(x.right)

    def postorder_tree_walk(self, x):
        if x is not None:
            self.inorder_tree_walk(x.left)
            self.inorder_tree_walk(x.right)
            print(x.key)

    def tree_search(self, x, k):
        if x is None or k == x.key:
            return x
        if k < x.key:
            return self.tree_search(x.left, k)
        else:
            return self.tree_search(x.right, k)

    @staticmethod
    def ite_tree_search(x, k):
        while x is not None and k != x.key:
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x

    @staticmethod
    def tree_min(x):
        while x.left is not None:
            x = x.left
        return x

    @staticmethod
    def tree_max(x):
        while x.right is not None:
            x = x.right
        return x

    def tree_successor(self, x):
        if x.right is not None:
            return self.tree_min(x.right)
        y = x.p
        while y is not None and x == y.right:
            x = y
            y = y.p
        return y

    def tree_predecessor(self, x):
        raise NotImplemented("TBI")

    def _preorder_tree_graph(self, x, G):
        if x is not None:
            G.add_node(x.key)
            if x.p is not None:
                G.add_edge(x.p.key, x.key)
            self._preorder_tree_graph(x.left, G)
            self._preorder_tree_graph(x.right, G)
        return G

    def draw(self, show=False):
        # raise NotImplemented("TBI")
        G = nx.DiGraph()
        self._preorder_tree_graph(self.root, G)
        if show:
            plt.figure(figsize=(8, 8))
            pos = graphviz_layout(G, prog='dot')
            nx.draw(G, pos, alpha=0.8, node_color="#1F5838",
                    with_labels=True)
            plt.axis('equal')
            plt.show()
        return G


class BinarySearchTree(BaseTree):

    def __init__(self, keys=None):
        self.root = None
        if keys is not None:
            for k in keys:
                self.tree_insert(k)

    def tree_insert(self, value):
        z = Node(value)
        self._tree_insert(z)

    def _tree_insert(self, z):
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y is None:
            self.root = z  # Tree was empty
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        return z

    def transplant(self, u, v):
        if u.p is None:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        if v is not None:
            v.p = u.p

    def tree_delete(self, z):
        if z.left is None:
            self.transplant(z, z.right)
        elif z.right is None:
            self.transplant(z, z.left)
        else:
            y = self.tree_min(z.right)
            if y.p != z:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.transplant(z, y)
            y.left = z.left
            y.left.p = y


class AVLTree(BinarySearchTree):

    # @staticmethod
    def balance_factor(self, x):
        # return self.tree_height(x.left) - self.tree_height(x.right)
        h_left, h_right = 0, 0
        if x.left:
            h_left = x.left.h
        if x.right:
            h_right = x.right.h
        return h_left - h_right

    def tree_insert(self, value):
        z = AVLNode(value)
        self._tree_insert(z)
        # z.h = self.tree_height(z)
        # Do post-balance check
        self.balance(z)

    def balance(self, x):
        while True:
            if x.p is None:
                break
            bf = self.balance_factor(x.p)
            # x.p.h = bf
            if bf <= -2:
                self.left_rotate(x.p)
            elif bf >= 2:
                self.right_rotate(x.p)
            if x.p is not None:
                x = x.p

    def left_rotate(self, x):
        y = x.right  # Set y
        x.right = y.left  # Turn y's left subtree into x's right subtree
        if y.left is not None:
            y.left.p = x
        y.p = x.p  # Link x's parent to y
        if x.p is None:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x  # Put x on y's left
        x.p = y
        # x.h = self.tree_height(x)
        # y.h = self.tree_height(y)

    def right_rotate(self, y):
        x = y.left  # Set x
        y.left = x.right  # Turn x's right subtree into y's left subtree
        if x.right is not None:
            x.right.p = y
        x.p = y.p  # Link y's parent to x
        if y.p is None:
            self.root = x
        elif y == y.p.right:
            y.p.right = x
        else:
            y.p.left = x
        x.right = y  # Put y on x's right
        y.p = x
        # x.h = self.tree_height(x)
        # y.h = self.tree_height(y)


if __name__ == '__main__':
    from alg_complexity.trees import AVLTree
    keys = [2, 5, 9, 12, 13, 15, 17, 18, 19]
    bst = AVLTree(keys)
    G = bst.draw(show=True)

