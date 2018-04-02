#!/usr/bin/env python3
# coding: utf8

"""
    Console application to analyse CSV Holter record.
"""

__version__ = '0.1'
__author__ = 'Matthieu Longo'

import datetime
import argparse
import logging
import os

import cardiologs.holter
import cardiologs.common.model.wave as wave
import cardiologs.measure as measure

import matplotlib.pyplot as plt


class CardioCharts(object):
    """
        Plot a chart for the whole record.
        It displays interesting data like :
        - heartrate (in heartbits / minute)
        - invalid waves (INV)
        - P waves tagged premature
        - QRS waves tagged premature
    """

    def __init__(self, begin, end):
        self._record_begin = begin
        self._record_end = end

    def plot_heartrate(self, xx, yy):
        lines = plt.plot(xx, yy)
        plt.setp(lines, color='blue', linewidth=0.5)
        plt.xlabel('time (day HH:MM::SS)')
        plt.ylabel('heartbits / minutes')

    def plot_INV(self, xx):
        plt.scatter(xx, list(map(lambda x: 10, xx)),
                    marker='o', s=1, c='black', label="INV")
        plt.legend()

    def plot_P_premature(self, xx):
        plt.scatter(xx, list(map(lambda x: 6, xx)),
                    marker='o', s=1, c='red', label='P premature')
        plt.legend()

    def plot_QRS_premature(self, xx):
        plt.scatter(xx, list(map(lambda x: 2, xx)),
                    marker='o', s=1, c='green', label='QRS premature')
        plt.legend()

    def show(self):
        plt.title('Heartrate record from {:%Y-%m-%d %H:%M:%S} to {:%Y-%m-%d %H:%M:%S}'
                  .format(self._record_begin, self._record_end))
        plt.show()


def run(args):
    """
    glue: main function
    """

    record_starttime = datetime.datetime.strptime(args.start_time, "%Y/%m/%d %H:%M:%S.%f")

    with cardiologs.holter.reader(args.file) as reader:

        measurements = measure.Measurements(record_starttime)

        for w in reader:
            measurements.update(w)

        print("Record start time: {}".format(record_starttime))
        print("Record end time: {}".format(measurements.time_last_sampling))

        summary = measurements.summary

        def to_HBpM(period):
            """
                Convert period in milliseconds to heartbits per minute
            """
            return round(1000 * 60 / period)

        def to_humanDate(timestamp):
            """
                Convert a timestamp to a human readable date
            """
            return record_starttime \
                 + datetime.timedelta(days=measure.ms_to_days(timestamp),
                                      seconds=measure.ms_to_secs(timestamp),
                                      milliseconds=timestamp)

        print("mean period QRS: {} ms".format(round(summary.average)))
        print("mean heartrate: {} heartbits/min"
              .format(to_HBpM(summary.average)))

        max_heartrate = to_HBpM(summary.min.value)
        min_heartrate = to_HBpM(summary.max.value)
        print("min heartrate: {}BpM ({})".format(min_heartrate, summary.max.time))
        print("max heartrate: {}BpM ({})".format(max_heartrate, summary.min.time))

        print("P: {}, QRS: {}, T: {}, INV: {}".format(len(measurements.P),
                                                      len(measurements.QRS),
                                                      len(measurements.T),
                                                      len(measurements.INV)))
        P_premature = list(filter(lambda x: wave.WaveTags.PREMATURE in x.tags, measurements.P))
        QRS_premature = list(filter(lambda x: wave.WaveTags.PREMATURE in x.tags, measurements.QRS))
        print("P premature: {}".format(len(P_premature)))
        print("QRS premature: {}".format(len(QRS_premature)))

        ######################
        # Draw charts
        ######################
        if args.plot_graph:
            charts = CardioCharts(record_starttime, measurements.time_last_sampling)

            # heart rates
            periods, timestamps = zip(*measurements.heartbit_periods)
            xx = list(map(to_humanDate, timestamps))
            yy = list(map(to_HBpM, periods))
            charts.plot_heartrate(xx, yy)

            # INV
            xx = list(map(lambda x: to_humanDate(x.timing.onset), measurements.INV))
            charts.plot_INV(xx)

            # P premature
            xx = list(map(lambda x: to_humanDate(x.timing.onset), P_premature))
            charts.plot_P_premature(xx)

            # Q premature
            xx = list(map(lambda x: to_humanDate(x.timing.onset), QRS_premature))
            charts.plot_QRS_premature(xx)

            charts.show()


def parse_args():
    """
        Parse the script arguments
    """
    def check_path(path):
        """
            Paths checker
        """
        if not os.path.exists(path):
            raise ValueError("{path} does not exist".format(path=path))
        return path

    parser = argparse.ArgumentParser(description="""Analyse CSV Holter
                                     record and print valuable information
                                      about delineation.""")
    parser.add_argument('-f', '--file', metavar='INFILE',
                        required=True,
                        type=check_path,
                        help='CSV Holter record')
    parser.add_argument('--plot-graph',
                        action='store_true',
                        help='Draw a graph')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Print debug information')
    parser.add_argument('-s', '--start-time', metavar='RECORD_START_TIME',
                        default="1970/01/01 00:00:00.000",
                        help="Record's start time")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    run(args)
