# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import numpy as np
import pendulum

from alg_complexity import datagen
from alg_complexity.trees import AVLTree
from alg_complexity.utils import class_execution_time, ClassExecTime

if __name__ == '__main__':
    now = pendulum.now()
    now_str = now.to_datetime_string()
    spath = Path('results', now_str)
    spath.mkdir(parents=True)
    cfg = {
        'n_min': 10**1,
        'n_max': 10**4,
        'n_measures': 20,
        'n_repeats': 2,
        'n_number': 5
    }

    sys.setrecursionlimit(cfg['n_max']*10)

    setups = [
        # ('random', lambda n: datagen.unique_integers(n, 0, 10000)),
        ('increasing', lambda n: datagen.range_n(n)),
        ('decreasing', lambda n: datagen.range_n_inv(n)),
    ]

    algorithms = [
        ('avl-tree-rec', {'method': 'search', 'method_kwargs': {'mode': 'recursive'}}),
        ('avl-tree-ite', {'method': 'search', 'method_kwargs': {'mode': 'iterative'}})
    ]
    for setup in setups:
        # setup_savename = '{setup[0]}-plot-{now}'.format(setup=setup,
        #                                                 now=now_str)
        # setup_savename = str(spath.joinpath(setup_savename))
        class_exec = ClassExecTime(AVLTree, setup[1])
        ns, exec_times = class_exec.exec_time(-10, algorithms, **cfg)
        savename = '{setup[0]}-res-{now}'.format(setup=setup, now=now_str)
        savename = str(spath.joinpath(savename))
        np.save(savename.replace('-res', '-times'), ns, allow_pickle=False)
        np.save(savename, exec_times, allow_pickle=False)
        np.save(savename.replace('-res', '-algs'), np.array([alg[0] for alg in algorithms]), allow_pickle=False)

        # for alg in algorithms:
        #     print('Running setup={setup[0]} -- alg={alg[0]}'.format(
        #         setup=setup, alg=alg))
        #     savename = '{setup[0]}-{alg[0]}-res-{now}'.format(setup=setup,
        #                                                       alg=alg,
        #                                                       now=now_str)
        #     savename = str(spath.joinpath(savename))
        #     ns, exec_times = class_exec.exec_time(-10, algorithms, **cfg)
        #     np.save(savename.replace('-res', '-times'), ns, allow_pickle=False)
        #     np.save(savename, exec_times, allow_pickle=False)
