#!/usr/bin/env python3
# coding: utf8

import cardiologs.strategy.csv_


class reader(object):
    """
    Cardiogram reader
    It adapts its strategy according to the file extension.
    For now, only CSV is supported.
    """

    _filename = None
    _reader_strategy = None

    def __init__(self, filepath):
        self._filepath = filepath
        if self._filepath.endswith('.csv'):
            fd = open(filepath, newline='', mode='r')
            self._reader_strategy = cardiologs.strategy.csv_.CSVReader(fd)
        else:
            raise IOError("unknown format")

    def __enter__(self):
        if self._reader_strategy:
            self._reader_strategy.__enter__()
        return self

    def __iter__(self):
        return self._reader_strategy

    def __next__(self):
        return next(self._reader_strategy)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._reader_strategy:
            self._reader_strategy.__exit__(exc_type, exc_val, exc_tb)
