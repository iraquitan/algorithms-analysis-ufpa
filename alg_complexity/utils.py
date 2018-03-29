# -*- coding: utf-8 -*-
from timeit import Timer
import numpy as np


def execution_time(func_handle, data, n_min=100, n_max=100000, n_measures=10,
                   n_repeats=1, n_number=1):

    class func_wrapper(object):

        def __init__(self, n):
            self.data = data

        def __call__(self):
            return func_handle(self.data)

    ns = np.linspace(n_min, n_max, n_measures)
    measures = np.zeros(n_measures)
    for i, n in enumerate(ns):
        timer = Timer(func_wrapper(100))
        measurements = timer.repeat(n_repeats, n_number)
