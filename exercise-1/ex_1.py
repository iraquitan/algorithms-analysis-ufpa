# -*- coding: utf-8 -*-
"""
Enunciado:
    Qual é o menor valor de entrada n (considere n > 0) tal que um algoritmo
    cujo tempo de execução é 10n2 é mais rápido que um algoritmo cujo tempo de
    execução é 2n na mesma máquina? Qual desses algoritmos você considera mais
    eficiente? Por quê?
"""

from sympy import symbols
from sympy.plotting import plot

n = symbols('n')
exp_1 = 10*(n*n)
exp_2 = 2**n
p1 = plot(exp_1, exp_2, (n, 0, 12), legend=True, show=False)
p1[1].line_color = 'r'
p1.show()

