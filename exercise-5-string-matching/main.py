# -*- coding: utf-8 -*-
from functools import partial
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pendulum

from alg_complexity import datagen
from alg_complexity.string_matching import bmh, bmhs, shift_and
from alg_complexity.utils import execution_time

if __name__ == '__main__':
    now = pendulum.now()
    now_str = now.to_datetime_string()
    spath = Path('results', now_str)
    spath.mkdir(parents=True)
    cfg = {
        'n_min': 10**1,
        'n_max': 10**7,
        'n_measures': 10,
        'n_repeats': 5,
        'n_number': 10
    }

    with open("messages_all.txt", 'r') as f:
        text = f.read()

    setups = [
        ('text', lambda n: text[0:n]),
    ]

    algorithms1 = [
        # ('BMH_padrao_incomun', partial(bmh, pattern='brazil')),
        # ('BMHS_padrao_incomun', partial(bmhs, pattern='brazil')),
        # ('Shift-And_padrao_incomun', partial(shift_and, pattern='brazil')),
    ]

    algorithms2 = [
        # ('BMH_padrao_comun', partial(bmh, pattern='2001-09-11')),
        # ('BMHS_padrao_comun', partial(bmhs, pattern='2001-09-11')),
        # ('Shift-And_padrao_comun', partial(shift_and, pattern='2001-09-11')),
    ]

    algorithms3 = [
        # ('BMH_padrao_inexistente', partial(bmh, pattern='iraquitan')),
        # ('BMHS_padrao_inexistente', partial(bmhs, pattern='iraquitan')),
        # ('Shift-And_padrao_inexistente', partial(shift_and, pattern='iraquitan')),
    ]

    algorithms4 = [
        ('BMH_padrao_comum2', partial(bmh, pattern=' ')),
        ('BMHS_padrao_comum2', partial(bmhs, pattern=' ')),
        ('Shift-And_padrao_comum2', partial(shift_and, pattern=' ')),
    ]

    algorithms = [
        # algorithms1,
        # algorithms2,
        # algorithms3,
        algorithms4
    ]

    for setup in setups:
        for algorithms_grp in algorithms:
            fig, ax = plt.subplots(1, 1)
            # setup_savename = f'{setup[0]}-plot-{now_str}'
            setup_savename = '{setup[0]}-plot-{now}'.format(setup=setup,now=now_str)
            setup_savename = str(spath.joinpath(setup_savename))
            for alg in algorithms_grp:
                print(f'Running setup={setup[0]} -- alg={alg[0]}')
                savename = f'{setup[0]}-{alg[0]}-res-{now_str}'
                # savename = '{setup[0]}-{alg[0]}-res-{now}'.format(setup=setup,alg=alg,now=now_str)
                savename = str(spath.joinpath(savename))
                ns, exec_times = execution_time(alg[1], setup[1], **cfg)
                np.save(savename.replace('-res', '-times'), ns, allow_pickle=False)
                np.save(savename, exec_times, allow_pickle=False)
                ax.plot(ns, exec_times, label=alg[0])

            ax.set_title(f'{setup[0]} input')
            ax.grid()
            ax.legend(loc='upper left', frameon=True)
            plt.tight_layout()
            plt.show()
            fig.savefig(setup_savename + '.svg', dpi=150)
