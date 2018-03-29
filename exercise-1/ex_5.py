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
from random import randint

import big_o


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
    positive_generator = lambda n: big_o.datagen.integers(1000, 0, 2**16)
    best_IS, others = big_o.big_o(insert_sort, positive_generator, n_repeats=1000)
    print(f'Insertion Sort: {best_IS}')

    best_BS, others = big_o.big_o(bubblesort, positive_generator, n_repeats=1000)
    print(f'Bubblesort: {best_BS}')

    best_SS, others = big_o.big_o(selection_sort, positive_generator, n_repeats=1000)
    print(f'Selection Sort: {best_SS}')
