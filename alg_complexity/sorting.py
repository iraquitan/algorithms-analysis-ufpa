# -*- coding: utf-8 -*-
__all__ = ['quicksort', 'heapsort']

from random import randint


def _partition(A, lo, hi):
    pivot = A[hi]
    i = lo - 1
    for j in range(lo, hi):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[hi] = A[hi], A[i+1]
    return i + 1


def _random_partition(A, lo, hi):
    i = randint(lo, hi)
    A[hi], A[i] = A[i], A[hi]
    return _partition(A, lo, hi)


def _mid_partition(A, lo, hi):
    i = lo+(hi-lo)//2
    A[hi], A[i] = A[i], A[hi]
    return _partition(A, lo, hi)


def _random_quicksort(A, lo=0, hi=0):
    if lo < hi:
        q = _random_partition(A, lo, hi)
        _random_quicksort(A, lo, q - 1)
        _random_quicksort(A, q + 1, hi)


def _mid_quicksort(A, lo=0, hi=0):
    if lo < hi:
        q = _mid_partition(A, lo, hi)
        _mid_quicksort(A, lo, q - 1)
        _mid_quicksort(A, q + 1, hi)


def _last_quicksort(A, lo=0, hi=0):
    if lo < hi:
        q = _partition(A, lo, hi)
        _last_quicksort(A, lo, q - 1)
        _last_quicksort(A, q + 1, hi)


def quicksort(A, mode='last'):
    if mode == 'last':
        _last_quicksort(A, lo=0, hi=len(A) - 1)
    elif mode == 'mid':
        _mid_quicksort(A, lo=0, hi=len(A) - 1)
    elif mode == 'random':
        _random_quicksort(A, lo=0, hi=len(A) - 1)


def _parent(i):
    return 1//2


def _left(i):
    return 2 * i


def _right(i):
    return 2 * i + 1


def _max_heapify(A, n, i):
    l = _left(i)
    r = _right(i)
    if l < n and A[l] > A[i]:
        largest = l
    else:
        largest = i
    if r < n and A[r] > A[largest]:
        largest = r
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        _max_heapify(A, n, largest)


def _max_heapify_it(A, n, i):
    while i < n:
        l = _left(i)
        r = _right(i)
        if l < n and A[l] > A[i]:
            largest = l
        else:
            largest = i
        if r < n and A[r] > A[largest]:
            largest = r
        if largest != i:
            A[i], A[largest] = A[largest], A[i]
            i = largest
        else:
            break


def _build_max_heap(A, mode='recursive'):
    n = len(A)
    for i in range(len(A)//2, 0-1, -1):
        if mode == 'recursive':
            _max_heapify(A, n, i)
        elif mode == 'iterative':
            _max_heapify_it(A, n, i)
        else:
            raise ValueError('"value" must be "recursive" or "iterative".')


def heapsort(A, mode='recursive'):
    _build_max_heap(A, mode)
    n = len(A)
    for i in range(n-1, 0, -1):
        A[0], A[i] = A[i], A[0]
        n -= 1
        if mode == 'recursive':
            _max_heapify(A, n, 0)
        elif mode == 'iterative':
            _max_heapify_it(A, n, 0)
        else:
            raise ValueError('"value" must be "recursive" or "iterative".')
