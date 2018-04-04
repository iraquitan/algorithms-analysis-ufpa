# -*- coding: utf-8 -*-
from timeit import Timer
import numpy as np


def execution_time(func_handle, datagen, n_min=100, n_max=100000, n_measures=10,
                   n_repeats=3, n_number=10**6):

    class func_wrapper(object):

        def __init__(self, n):
            self.data = datagen(n)

        def __call__(self):
            return func_handle(self.data)

    ns = np.linspace(n_min, n_max, n_measures, dtype=int)
    # ns = np.array([10**j for j in range(1, 6)])
    execution_time = np.zeros(n_measures)
    for i, n in enumerate(ns):
        print(f'Running for n={n}')
        timer = Timer(func_wrapper(n))
        measurements = timer.repeat(n_repeats, n_number)
        execution_time[i] = np.min(measurements)
    return ns, execution_time
