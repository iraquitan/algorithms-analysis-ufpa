# -*- coding: utf-8 -*-
from sympy import symbols, latex
from sympy.plotting import plot

n = symbols('n')
exp_0 = 0.5*(n*n)-3*n
exp_1 = n*n
p1 = plot(exp_0, exp_1, (n, 0, 13), legend=True, show=False)
p1[1].line_color = 'r'
p1[0].label = f'${latex(exp_0)}$'
p1[1].label = f'${latex(exp_1)}$'
p1.show()
