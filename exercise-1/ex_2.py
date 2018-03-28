# -*- coding: utf-8 -*-
"""
Enunciado:
    Implemente em qualquer linguagem de programação um programa para verificar
    se o valor de entrada é, ou não, um nú́mero primo. Existe pior e melhor
    caso? Quais são eles?
"""
import big_o
from random import randint


def is_prime(x):
    for i in range(2, x + 1):
        if x % i == 0 and i != x:
            return False
    return True


if __name__ == '__main__':
    positive_n_generator = lambda n: big_o.datagen.n_(randint(1, 2**20))
    best, others = big_o.big_o(is_prime, positive_n_generator, n_repeats=10000)
    print(best)
    for class_, residuals in others.items():
        print('{0} (res {1:.2G})'.format(class_, residuals))
