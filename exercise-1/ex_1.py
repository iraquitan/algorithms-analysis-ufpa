# -*- coding: utf-8 -*-
"""
Enunciado:
    Qual é o menor valor de entrada n (considere n > 0) tal que um algoritmo
    cujo tempo de execução é 10n2 é mais rápido que um algoritmo cujo tempo de
    execução é 2n na mesma máquina? Qual desses algoritmos você considera mais
    eficiente? Por quê?
"""
from matplotlib import style
style.use('seaborn-whitegrid')
from sympy import symbols, latex
from sympy.plotting import plot


if __name__ == '__main__':
    n = symbols('n')
    exp_0 = 10 * (n * n)
    exp_1 = 2 ** n
    p1 = plot(exp_0, exp_1, (n, 0, 13), legend=True, show=False, xlabel='Input size(n)', ylabel='# of Instructions')
    p1[1].line_color = 'r'
    p1[0].label = f'A: ${latex(exp_0)}$'
    p1[1].label = f'B: ${latex(exp_1)}$'
    p1.show()
