# -*- coding: utf-8 -*-
"""
Enunciado:
    Qual é o menor valor de entrada n (considere n > 0) tal que um algoritmo
    cujo tempo de execução é 10n2 é mais rápido que um algoritmo cujo tempo de
    execução é 2n na mesma máquina? Qual desses algoritmos você considera mais
    eficiente? Por quê?
"""

from sympy import symbols, latex
from sympy.plotting import plot

n = symbols('n')
exp_0 = 10*(n*n)
exp_1 = 2**n
p1 = plot(exp_0, exp_1, (n, 0, 13), legend=True, show=False)
p1[1].line_color = 'r'
p1[0].label = f'${latex(exp_0)}$'
p1[1].label = f'${latex(exp_1)}$'
p1.show()
