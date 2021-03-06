# -*- coding: utf-8 -*-

import random
import string


def n_(n):
    """ Return N. """
    return n


def range_n(n, start=0, step=1):
    """ Return the sequence [start, start+1, ..., start+N-1]. """
    return list(range(start, start+n, step))


def range_n_inv(n, end=0, step=-1):
    """ Return the sequence [start, start+1, ..., start+N-1]. """
    return list(range(n, end, step))


def integers_equal(n, min_, max_):
    """ Return sequence of N equal integers between min_ and max_ (included).
    """
    eq = random.randint(min_, max_)
    return [eq for _ in range(n)]


def integers(n, min_, max_):
    """ Return sequence of N random integers between min_ and max_ (included).
    """
    return [random.randint(min_, max_) for _ in range(n)]


def unique_integers(n, min_, max_):
    """ Return sequence of N random integers between min_ and max_ (included).
    """
    un = list({random.randint(min_, max_) for _ in range(n)})
    random.shuffle(un)
    return un


def large_integers(n):
    """ Return sequence of N large random integers. """
    return [random.randint(-50, 50) * 1000000 + random.randint(0, 10000)
            for _ in range(n)]


def strings(n, chars=string.ascii_letters):
    """ Return random string of N characters, sampled at random from `chars`.
    """
    return ''.join([random.choice(chars) for i in range(n)])
