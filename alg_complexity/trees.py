# -*- coding: utf-8 -*-


class Node(object):
    def __init__(self, key, left=None, right=None, p=None):
        self.key = key
        self.left = left
        self.right = right
        self.p = p

    def __repr__(self):
        return f"Node[{self.key}]"


class AVLNode(Node):
    def __init__(self, key, left=None, righ=None, p=None):
        super(AVLNode, self).__init__(key, left, righ, p)
        self.h = 0

    def __repr__(self):
        return f"Node[{self.key}, h={self.h}]"


class BaseTree(object):

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

    def tree_height(self, x):
        if x is None:
            return -1
        else:
            return max(self.tree_height(x.left), self.tree_height(x.right)) + 1

    def print(self):
        raise NotImplemented("TBI")


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

    def balance_factor(self, x):
        return self.tree_height(x.left) - self.tree_height(x.right)

    def tree_insert(self, value):
        z = AVLNode(value)
        self._tree_insert(z)
        # Do post-balance check

    def balance(self, x):
        while x is not None:
            self.balance_factor(x)

