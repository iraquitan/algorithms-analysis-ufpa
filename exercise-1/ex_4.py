# -*- coding: utf-8 -*-
"""
Enunciado:
    Cada um dos algoritmos abaixo recebe um inteiro positivo e devolve outro
    inteiro positivo. Os dois algoritmos devolvem o mesmo número se receberem
    o mesmo valor de entrada 'n'? Qual dos dois algoritmos é mais eficiente?
    Por quê?
"""
from random import randint

import big_o


def square_sum_a(n):
    x = 0
    for j in range(n+1):
        x += j * j
    return x


def square_sum_b(n):
    x = n * (n + 1) * (2 * n + 1)
    x = x / 6
    return x


if __name__ == '__main__':
    # positive_n_generator = lambda n: big_o.datagen.n_(randint(1, 2**16))
    # best, others = big_o.big_o(square_sum_a, positive_n_generator, n_repeats=1000)
    # print(f'A: {best}')
    #
    # # positive_n_generator = lambda n: big_o.datagen.n_(randint(1, 2**20))
    # best, others = big_o.big_o(square_sum_b, positive_n_generator, n_repeats=1000)
    # print(f'B: {best}')
    # print(square_sum_a(10))
    # print(square_sum_b(10))
    x = 12312341341
    print(square_sum_a(x))
    print(square_sum_b(x))
