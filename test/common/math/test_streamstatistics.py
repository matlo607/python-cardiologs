#!/usr/bin/env python3
# coding: utf8

import unittest

import cardiologs.common.math.streamstatistics as streamstats


class StreamStatisticsTest(unittest.TestCase):

    def test_movingAverage(self):
        computeAverage = streamstats.MovingAverage()
        self.assertEqual(computeAverage.value, 0)

        samples = [-1, 5, 6, 10, 2, 5, 4, 0, 0, 9]
        expected_averages = [-1, 2, 10/3, 5, 4.4, 4.5, 31/7, 31/8, 31/9, 4]

        for i in range(0, len(samples)):
            average = computeAverage(samples[i])
            self.assertEqual(average, expected_averages[i])

        self.assertEqual(computeAverage.value, expected_averages[-1])

    def test_periodComputer(self):
        computePeriod = streamstats.PeriodComputer()
        t = [1.5, 3.5, 5.5, 7, 10, 13]
        periods = [0, 2, 2, 1.5, 3, 3]
        for i in range(0, len(t)):
            period = computePeriod(t[i])
            self.assertEqual(period, periods[i])

    def test_movingMax(self):
        computeMax = streamstats.MovingMax()
        n = [4, 5, 4, 3, 9, -1, 78, 6]
        expected_maxs = [
            (4, True),
            (5, True),
            (5, False),
            (5, False),
            (9, True),
            (9, False),
            (78, True),
            (78, False)
        ]

        for i in range(0, len(n)):
            found_new_max = computeMax(n[i])
            self.assertEqual(computeMax.value, expected_maxs[i][0])
            self.assertEqual(found_new_max, expected_maxs[i][1])
        self.assertEqual(computeMax.value, expected_maxs[-1][0])

    def test_movingMin(self):
        computeMin = streamstats.MovingMin()
        n = [4, 5, 4, 3, 9, -1, 78, 6]
        expected_mins = [
            (4, True),
            (4, False),
            (4, False),
            (3, True),
            (3, False),
            (-1, True),
            (-1, False),
            (-1, False)
        ]

        for i in range(0, len(n)):
            found_new_min = computeMin(n[i])
            self.assertEqual(computeMin.value, expected_mins[i][0])
            self.assertEqual(found_new_min, expected_mins[i][1])
        self.assertEqual(computeMin.value, expected_mins[-1][0])


if __name__ == '__main__':
    unittest.main()
