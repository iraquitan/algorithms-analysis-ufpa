# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import numpy as np
import pendulum

from alg_complexity import datagen
from alg_complexity.trees import AVLTree
from alg_complexity.utils import class_execution_time

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
        # ('random', lambda n: datagen.unique_integers(n, 0, 10000)),
        ('increasing', lambda n: datagen.range_n(n)),
        ('decreasing', lambda n: datagen.range_n_inv(n)),
    ]

    algorithms = [
        ('avl-tree-rec', AVLTree, 'search', {'mode': 'recursive'}),
        ('avl-tree-ite', AVLTree, 'search', {'mode': 'iterative'})
    ]
    for setup in setups:
        # fig, ax = plt.subplots(1, 1)
        # setup_savename = f'{setup[0]}-plot-{now_str}'
        setup_savename = '{setup[0]}-plot-{now}'.format(setup=setup,now=now_str)
        setup_savename = str(spath.joinpath(setup_savename))
        for alg in algorithms:
            # print(f'Running setup={setup[0]} -- alg={alg[0]}')
            print('Running setup={setup[0]} -- alg={alg[0]}'.format(setup=setup,alg=alg))
            # savename = f'{setup[0]}-{alg[0]}-res-{now_str}'
            savename = '{setup[0]}-{alg[0]}-res-{now}'.format(setup=setup,alg=alg,now=now_str)
            savename = str(spath.joinpath(savename))
            ns, exec_times = class_execution_time(alg[1], setup[1], alg[2],
                                                  alg[3], -12, **cfg)
            np.save(savename.replace('-res', '-times'), ns, allow_pickle=False)
            np.save(savename, exec_times, allow_pickle=False)
