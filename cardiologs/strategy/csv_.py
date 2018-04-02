#!/usr/bin/env python3
# coding: utf8

import csv
import logging

import cardiologs.common.model.wave as wave


class CSVReader(object):
    """
    Encapsulate CSV reader and the rules to store waves in CSV.
    """

    def __init__(self, fd):
        self._csvfile = fd
        sample = self._csvfile.readline()
        if not sample:
            logging.error("csv file is empty")
            raise IOError("Empty file")
        dialect = csv.Sniffer().sniff(sample)
        self._csvfile.seek(0)
        self._wave_reader = csv.reader(self._csvfile, dialect=dialect)

    def __import(self, csv_wave):
        wave_type_mapper = {
            "INV": wave.WaveType.INV,
            "P": wave.WaveType.P,
            "QRS": wave.WaveType.QRS,
            "T": wave.WaveType.T
        }

        wave_tags_mapper = {
            "aberration": wave.WaveTags.ABERRATION,
            "ectopic": wave.WaveTags.ECTOPIC,
            "junctional": wave.WaveTags.JUNCTIONAL,
            "manual": wave.WaveTags.MANUAL,
            "non-conducted": wave.WaveTags.NONCONDUCTED,
            "paced": wave.WaveTags.PACED,
            "premature": wave.WaveTags.PREMATURE
        }

        tags = None
        try:
            tags = list(map(lambda x: wave_tags_mapper[x], csv_wave[3:]))
        except KeyError as e:
            logging.error("unknown tag: {}".format(e))

        return wave.Wave(wave_type_mapper[csv_wave[0]],
                         wave.WaveTiming(onset=float(csv_wave[1]),
                                         offset=float(csv_wave[2])),
                         tags)

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def __next__(self):
        csv_wave = next(self._wave_reader)
        logging.debug("wave = {}".format(csv_wave))
        return self.__import(csv_wave)

    def __exit__(self, type_, value, traceback):
        self._csvfile.close()
