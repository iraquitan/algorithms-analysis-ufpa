# -*- coding: utf-8 -*-
from timeit import Timer
import numpy as np


def execution_time(func_handle, datagen, n_min=100, n_max=100000, n_measures=10,
                   n_repeats=3, n_number=10**6):

    class FuncWrapper:

        def __init__(self, n):
            self.data = datagen(n)

        def __call__(self):
            return func_handle(self.data)

    ns = np.linspace(n_min, n_max, n_measures, dtype=int)
    # ns = np.array([10**j for j in range(1, 6)])
    execution_time = np.zeros(n_measures)
    for i, n in enumerate(ns):
        print(f'Running for n={n}')
        timer = Timer(FuncWrapper(n), )
        measurements = timer.repeat(n_repeats, n_number)
        execution_time[i] = np.min(measurements) / n_number
    return ns, execution_time


def class_execution_time(class_handle, datagen, method_name, method_kwargs,
                         method_data, n_min=100, n_max=100000, n_measures=10,
                         n_repeats=3, n_number=10**6):

    class ClassInit:
        def __init__(self, n):
            self.data = datagen(n)
            self.obj = class_handle(self.data)

    class ClassWrapper:
        def __init__(self, obj, data):
            self.obj = obj
            self.data = data

        def __call__(self):
            return getattr(self.obj, method_name)(self.data, **method_kwargs)

    ns = np.linspace(n_min, n_max, n_measures, dtype=int)
    execution_time = np.zeros(n_measures)
    for i, n in enumerate(ns):
        print(f'Running for n={n}')
        cls_obj = ClassInit(n)
        timer = Timer(ClassWrapper(cls_obj.obj, method_data), )
        measurements = timer.repeat(n_repeats, n_number)
        execution_time[i] = np.min(measurements) / n_number
    return ns, execution_time
