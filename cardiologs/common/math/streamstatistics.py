#!/usr/bin/env python3
# coding: utf8

import sys


class MovingAverage(object):
    """
        Compute the average on a moving stream of samples
    """

    def __init__(self):
        self._sum = 0
        self._nsamples = 0

    def __call__(self, newsample):
        self._nsamples += 1
        self._sum += newsample
        return self._sum / self._nsamples

    @property
    def value(self):
        return self._sum / self._nsamples if self._nsamples != 0 else 0


class PeriodComputer(object):

    def __init__(self):
        self._prev = 0

    def __call__(self, newtime):
        if self._prev == 0:
            self._prev = newtime
            return 0

        period = newtime - self._prev
        self._prev = newtime
        return period


class MovingMax(object):

    def __init__(self):
        self._max = -sys.maxsize

    def __call__(self, candidate):
        if self._max < candidate:
            self._max = candidate
            return True
        return False

    @property
    def value(self):
        return self._max


class MovingMin(object):
    def __init__(self):
        self._min = sys.maxsize

    def __call__(self, candidate):
        if self._min > candidate:
            self._min = candidate
            return True
        return False

    @property
    def value(self):
        return self._min
