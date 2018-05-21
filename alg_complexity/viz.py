from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


SETUPS = ['random', 'increasing', 'decreasing', 'equal']
# SETUPS = ['equal']
ALGS = ['quicksort-mid', 'quicksort-rand', 'heapsort-ite', 'heapsort-rec']
# ALGS = ['heapsort-ite', 'heapsort-rec']
# ALGS = ['quicksort-mid', 'quicksort-rand']


def plot_results(res_path, setups, algs, show=False):
    p = Path(res_path)
    for s in setups:
        fig, ax = plt.subplots(1, 1)
        for a in algs:
            files = list(p.glob('**/*{s}*{a}*.npy'.format(s=s, a=a)))
            if len(files) == 0:
                continue
            plot_data = {}
            for f in files:
                if '-res-' in str(f):
                    plot_data['res'] = np.load(f)
                elif '-times-' in str(f):
                    plot_data['times'] = np.load(f)
            ax.plot(plot_data['times'], plot_data['res'], label=a)
        ax.set_title(f'{s} input')
        ax.set_xlabel('Tamanho do Vetor de Entrada')
        ax.set_ylabel('Tempo de Execução (s)')
        ax.grid()
        ax.legend(loc='upper left', frameon=True)
        plt.tight_layout()
        if show:
            plt.show()
        fig.savefig(p.joinpath(f'{s}-plot' + '.svg'), dpi=150)
