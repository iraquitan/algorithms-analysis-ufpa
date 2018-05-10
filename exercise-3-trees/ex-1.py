# -*- coding: utf-8 -*-
from alg_complexity.trees import AVLTree, BlackRedTree


if __name__ == '__main__':
    keys = [30, 25, 45, 15, 41, 56, 35, 43, 50]
    avl = AVLTree(keys, debug=True)
    avl.draw(show=True)
    # Insert
    for k in [49, 60, 65]:
        avl.tree_insert(k)
        avl.draw(show=True)
    # Delete
    for k in [45, 41]:
        z = avl.tree_delete(k)
        if z:
            avl.draw(show=True)
    print("")
