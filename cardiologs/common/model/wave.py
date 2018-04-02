#!/usr/bin/env python3
# coding: utf8

from enum import Enum, auto, unique
from collections import namedtuple


@unique
class WaveType(Enum):
    P = auto()
    QRS = auto()
    T = auto()
    INV = auto()


@unique
class WaveTags(Enum):
    ABERRATION = auto()
    ECTOPIC = auto()
    JUNCTIONAL = auto()
    MANUAL = auto()
    NONCONDUCTED = auto()
    PACED = auto()
    PREMATURE = auto()


WaveTiming = namedtuple('WaveTiming', ['onset', 'offset'])


class Wave(object):
    """
    A wave is classified through its :
    - type (P,QRS,T,INV)
    - the length of a pulse (start time and end time)
    - tag (optional)
    """

    def __init__(self, type_, timing, tags=None):
        self._type = type_
        self._timing = timing
        self._tags = tags

    @property
    def type(self):
        return self._type

    @property
    def timing(self):
        return self._timing

    @property
    def tags(self):
        return list() if self._tags is None else self._tags

    def __repr__(self):
        return "{}: onset = {}, offset = {} {}".format(self._type,
                                                       self.timing.onset,
                                                       self.timing.offset,
                                                       self.tags)
