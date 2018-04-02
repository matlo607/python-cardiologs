#!/usr/bin/env python3
# coding: utf8

import datetime
from collections import namedtuple

import cardiologs.common.model.wave as wave
import cardiologs.common.math.streamstatistics as cardiomath


def ms_to_secs(ms):
    """
    Convert milliseconds to seconds
    """
    return ms / 1000


def ms_to_days(ms):
    """
    Convert milliseconds to days
    """
    return ms_to_secs(ms) / (3600 * 24)


Max = namedtuple('Max', ['value', 'time'])
Min = namedtuple('Min', ['value', 'time'])
Summary = namedtuple('Summary', ['average', 'min', 'max'])


class Measurements(object):
    """
    Aggregate various measures together
    """
    _P = list()
    _QRS = list()
    _INV = list()
    _T = list()
    _heartbit_periods = list()

    def __init__(self, timeoffset):
        self._period = cardiomath.PeriodComputer()
        self._average = cardiomath.MovingAverage()
        self._max = cardiomath.MovingMax()
        self._min = cardiomath.MovingMin()

        self._timeoffset = timeoffset
        self._time_last_sampling = timeoffset
        self._time_max = None
        self._time_min = None

    def update(self, w):
        if w.type == wave.WaveType.QRS:
            last_sampling = datetime.timedelta(days=ms_to_days(w.timing.onset),
                                               seconds=ms_to_secs(w.timing.onset),
                                               milliseconds=w.timing.onset)
            self._time_last_sampling = self._timeoffset + last_sampling

            period = self._period(w.timing.onset)
            if period != 0:
                self._average(period)
                if self._min(period):
                    sample_date = datetime.timedelta(days=ms_to_days(w.timing.onset),
                                                     seconds=ms_to_secs(w.timing.onset),
                                                     milliseconds=w.timing.onset)
                    self._time_min = self._timeoffset + sample_date
                if self._max(period):
                    sample_date = datetime.timedelta(days=ms_to_days(w.timing.onset),
                                                     seconds=ms_to_secs(w.timing.onset),
                                                     milliseconds=w.timing.onset)
                    self._time_max = self._timeoffset + sample_date
                self._heartbit_periods.append((period, w.timing.onset))

        if w.type == wave.WaveType.P:
            self._P.append(w)
        elif w.type == wave.WaveType.QRS:
            self._QRS.append(w)
        elif w.type == wave.WaveType.INV:
            self._INV.append(w)
        elif w.type == wave.WaveType.T:
            self._T.append(w)

    @property
    def summary(self):
        return Summary(average=self._average.value,
                       min=Min(value=self._min.value, time=self._time_min),
                       max=Max(value=self._max.value, time=self._time_max))

    @property
    def P(self):
        return self._P

    @property
    def QRS(self):
        return self._QRS

    @property
    def INV(self):
        return self._INV

    @property
    def T(self):
        return self._T

    @property
    def time_last_sampling(self):
        return self._time_last_sampling

    @property
    def heartbit_periods(self):
        return self._heartbit_periods
