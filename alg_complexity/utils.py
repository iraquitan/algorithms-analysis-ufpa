# -*- coding: utf-8 -*-
from functools import partial
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


class ClassExecTime:

    def __init__(self, class_, datagen):
        """"""
        self.datagen = datagen
        self.class_ = class_
        self.data = None
        self.obj = None

    def class_init(self, n):
        self.data = self.datagen(n)
        self.obj = self.class_(self.data)
    
    def call_method(self, call_data, method, method_kwargs):
        if self.data and self.obj:
            return getattr(self.obj, method)(call_data, **method_kwargs)
        else:
            raise RuntimeError('Should initialize class first with '
                               '"class_init"')

    def exec_time(self, call_data, methods, n_min=100,
                  n_max=100000, n_measures=10, n_repeats=3, n_number=10**6):
        ns = np.linspace(n_min, n_max, n_measures, dtype=int)
        exec_times = np.zeros((len(methods), n_measures))
        for i, n in enumerate(ns):
            print(f'Running for n={n}')
            self.class_init(n)
            for j, (_, method) in enumerate(methods):
                timer = Timer(partial(self.call_method, call_data=call_data, **method), )
                measurements = timer.repeat(n_repeats, n_number)
                exec_times[j, i] = np.min(measurements) / n_number
        return ns, exec_times


class ExecTime:

    def __init__(self, class_, datagen):
        """"""
        self.datagen = datagen
        self.class_ = class_
        self.data = None
        self.obj = None

    def set_up(self, n):
        self.data = self.datagen(n)
        self.obj = self.class_(self.data)

    def call_method(self, call_data, method, method_kwargs):
        if self.obj is None:
            self.obj = self.class_()
        return getattr(self.obj, method)(call_data, **method_kwargs)

    def exec_time(self, call_data, method, n_min=100,
                  n_max=100000, n_measures=10, n_repeats=3, n_number=10**6):
        ns = np.linspace(n_min, n_max, n_measures, dtype=int)
        exec_times = np.zeros(n_measures)
        for i, n in enumerate(ns):
            print(f'Running for n={n}')
            # self.class_init(n)
            timer = Timer(partial(self.call_method, call_data=call_data(n), **method), )
            self.obj = None
            measurements = timer.repeat(n_repeats, n_number)
            exec_times[i] = np.min(measurements) / n_number
        return ns, exec_times
