# -*- coding: utf-8 -*-
"""
Enunciado:
    Compare assintoticamente o tempo de execução (apresente dados, tabelas e
    gráficos) dos algoritmos de ordenação:
        Inserção; BubbleSort; e Seleção.
    Em seguida, responda os seguintes questionamentos.
        a. Qual desses algoritmos é o mais eficiente?
        b. A ordem inicial do vetor de entrada influencia no desempenho dos
            algoritmos?
        c. Qual desses algoritmos você usaria na sua aplicação?
"""
import matplotlib.pyplot as plt
import numpy as np
# import big_o

from alg_complexity import datagen
from alg_complexity.utils import execution_time


def insert_sort(A):
    for j in range(1, len(A)):
        key = A[j]
        # Insert A[j]  into the sorted sequence A[1..j-1].
        i = j - 1
        while i >= 0 and A[i] > key:
            A[i + 1] = A[i]
            i -= 1
        A[i + 1] = key
    return A


def bubblesort(A):
    for i in range(len(A)):
        for j in range(len(A) - 1, i, -1):
            if A[j] < A[j - 1]:
                A[j], A[j - 1] = A[j - 1], A[j]
    return A


def selection_sort(A):
    for i in range(len(A)):
        min_ix = i
        for j in range(i+1, len(A)):
            if A[j] < A[min_ix]:
                min_ix = j
        if min_ix != i:
            A[i], A[min_ix] = A[min_ix], A[i]
    return A


if __name__ == '__main__':
    n_min = 10**1
    n_max = 10**4
    n_measures = 20
    n_repeats = 1
    n_timings = 5
    # pos_int_gen = lambda n: datagen.integers(n, 0, 10000)
    # # pos_int_gen2 = lambda n: datagen.range_n_inv(n)
    # ns, IS_exec_times = execution_time(insert_sort, pos_int_gen, n_min, n_max, n_measures,
    #                                    n_repeats, n_timings)
    # np.save('ns_results4', ns, allow_pickle=False)
    # np.save('IS_results4', IS_exec_times, allow_pickle=False)
    #
    # _, BS_exec_times = execution_time(bubblesort, pos_int_gen, n_min, n_max, n_measures,
    #                                   n_repeats, n_timings)
    # np.save('BS_results4', BS_exec_times, allow_pickle=False)
    #
    # _, SS_exec_times = execution_time(selection_sort, pos_int_gen, n_min, n_max, n_measures,
    #                                   n_repeats, n_timings)
    # np.save('SS_results4', SS_exec_times, allow_pickle=False)

    IS_exec_times = np.load('./IS_results.npy')
    ns = np.load('./ns_results.npy')
    BS_exec_times = np.load('./BS_results.npy')
    SS_exec_times = np.load('./SS_results.npy')

    plt.plot(ns, IS_exec_times, label='Insertion Sort')
    plt.plot(ns, BS_exec_times, label='Bubble Sort')
    plt.plot(ns, SS_exec_times, label='Selection Sort')
    plt.grid()
    plt.legend()
    plt.show()

    # positive_generator = lambda n: big_o.datagen.integers(1000, 0, 2**16)
    # best_IS, others = big_o.big_o(insert_sort, positive_generator, n_repeats=1000)
    # print(f'Insertion Sort: {best_IS}')
    #
    # best_BS, others = big_o.big_o(bubblesort, positive_generator, n_repeats=1000)
    # print(f'Bubblesort: {best_BS}')
    #
    # best_SS, others = big_o.big_o(selection_sort, positive_generator, n_repeats=1000)
    # print(f'Selection Sort: {best_SS}')
