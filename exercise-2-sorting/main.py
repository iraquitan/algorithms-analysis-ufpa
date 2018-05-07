# -*- coding: utf-8 -*-
import sys
from functools import partial
from pathlib import Path

# import matplotlib.pyplot as plt
import numpy as np
import pendulum

sys.path.append('/Users/iraquitan/Developer/algorithms-analysis-ufpa/')
from alg_complexity.sorting import quicksort, heapsort
from alg_complexity import datagen
from alg_complexity.utils import execution_time


if __name__ == '__main__':
    now = pendulum.now()
    now_str = now.to_datetime_string()
    spath = Path('results', now_str)
    spath.mkdir(parents=True)
    cfg = {
        'n_min': 10**1,
        'n_max': 2*10**5,
        'n_measures': 20,
        'n_repeats': 10,
        'n_number': 20
    }

    sys.setrecursionlimit(cfg['n_max']*10)

    setups = [
        ('random', lambda n: datagen.integers(n, 0, 10000)),
        ('increasing', lambda n: datagen.range_n(n)),
        ('decreasing', lambda n: datagen.range_n_inv(n)),
        # ('equal', lambda n: datagen.integers_equal(n, 0, 10000))
    ]

    algorithms = [
        ('quicksort-mid', partial(quicksort, mode='mid')),
        ('quicksort-rand', partial(quicksort, mode='random')),
        ('heapsort-rec', partial(heapsort, mode='recursive')),
        ('heapsort-ite', partial(heapsort, mode='iterative'))
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
            ns, exec_times = execution_time(alg[1], setup[1], **cfg)
            np.save(savename.replace('-res', '-times'), ns, allow_pickle=False)
            np.save(savename, exec_times, allow_pickle=False)
            # ax.plot(ns, exec_times, label=alg[0])

        # ax.set_title(f'{setup[0]} input')
        # ax.grid()
        # ax.legend(loc='upper left', frameon=True)
        # plt.tight_layout()
        # plt.show()
        # fig.savefig(setup_savename + '.svg', dpi=150)

    # # B = [randint(0, 10**2) for n in range(10**1)]
    # B = setups[1][1](10**3)
    # # C = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
    # C = B.copy()
    # print(f"before quicksort: {B}")
    # quicksort(B, mode='mid')
    # print(f"after quicksort: {B}")
    #
    # print(f"\nbefore heapsort: {C}")
    # heapsort(C, mode='iterative')
    # print(f"after heapsort: {C}")
    #
    # print(f"B == C: {B == C}")