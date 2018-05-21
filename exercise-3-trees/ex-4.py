# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from random import choice

import numpy as np
import pendulum

from alg_complexity import datagen
from alg_complexity.trees import AVLTree, RedBlackTree
from alg_complexity.utils import class_execution_time, ClassExecTime, ExecTime

if __name__ == '__main__':
    now = pendulum.now()
    now_str = now.to_datetime_string()
    spath = Path('results', now_str)
    spath.mkdir(parents=True)
    cfg = {
        'n_min': 10**1,
        'n_max': 2*10**5,
        'n_measures': 20,
        'n_repeats': 5,
        'n_number': 10
    }

    sys.setrecursionlimit(cfg['n_max']*10)

    setups = [
        # ('unique-random', lambda n: datagen.unique_integers(n, 0, n*3)),
        ('increasing', lambda n: datagen.range_n(n)),
        # ('decreasing', lambda n: datagen.range_n_inv(n)),
    ]

    algorithms = [
        ('avl-tree-insert', AVLTree, {'method': '_add_keys', 'method_kwargs': {}}),
        ('rb-tree-insert', RedBlackTree, {'method': '_add_keys', 'method_kwargs': {}})
    ]
    algorithms_2 = [
        ('avl-tree-delete', AVLTree, {'method': 'tree_delete', 'method_kwargs': {}}),
        ('rb-tree-delete', RedBlackTree, {'method': 'tree_delete', 'method_kwargs': {}})
    ]

    algorithms_3 = [
        ('avl-tree-search', AVLTree, {'method': 'search', 'method_kwargs': {}}),
        ('rb-tree-search', RedBlackTree, {'method': 'search', 'method_kwargs': {}})
    ]
    for setup in setups:
        for alg in algorithms:
            class_exec = ExecTime(alg[1], setup[1])
            print('Running setup={setup[0]} -- alg={alg[0]}'.format(
                setup=setup, alg=alg))
            savename = '{setup[0]}-{alg[0]}-res-{now}'.format(setup=setup,
                                                              alg=alg,
                                                              now=now_str)
            savename = str(spath.joinpath(savename))
            ns, exec_times = class_exec.exec_time(setup[1], alg[-1], **cfg)
            np.save(savename.replace('-res', '-times'), ns, allow_pickle=False)
            np.save(savename, exec_times, allow_pickle=False)

        for alg in algorithms_2:
            class_exec = ClassExecTime(alg[1], setup[1])
            print('Running setup={setup[0]} -- alg={alg[0]}'.format(
                setup=setup, alg=alg))
            savename = '{setup[0]}-{alg[0]}-res-{now}'.format(setup=setup,
                                                              alg=alg,
                                                              now=now_str)
            savename = str(spath.joinpath(savename))
            ns, exec_times = class_exec.exec_time(choice, alg[-1], **cfg)
            np.save(savename.replace('-res', '-times'), ns, allow_pickle=False)
            np.save(savename, exec_times, allow_pickle=False)

        for alg in algorithms_3:
            class_exec = ClassExecTime(alg[1], setup[1])
            print('Running setup={setup[0]} -- alg={alg[0]}'.format(
                setup=setup, alg=alg))
            savename = '{setup[0]}-{alg[0]}-res-{now}'.format(setup=setup,
                                                              alg=alg,
                                                              now=now_str)
            savename = str(spath.joinpath(savename))
            ns, exec_times = class_exec.exec_time(-99, alg[-1], **cfg)
            np.save(savename.replace('-res', '-times'), ns, allow_pickle=False)
            np.save(savename, exec_times, allow_pickle=False)
