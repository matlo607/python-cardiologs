#!/usr/bin/env python3
# coding: utf8

import unittest
import logging
import io

import cardiologs.common.model.wave as wave
import cardiologs.strategy.csv_ as stcsv

class StrategyCsvTest(unittest.TestCase):

    def test_empty_file(self):
        csvinput = io.StringIO("")
        with self.assertRaises(IOError):
            reader = stcsv.CSVReader(csvinput)

    def test_onerow_file(self):
        csvinput = io.StringIO("INV,92,248")
        with stcsv.CSVReader(csvinput) as reader:
            waves = list()
            for data in reader:
                waves.append(data)
            self.assertEqual(len(waves), 1)
            w = waves[0]
            self.assertEqual(w.type, wave.WaveType.INV)
            self.assertEqual(w.timing.onset, 92.0)
            self.assertEqual(w.timing.offset, 248.0)
            self.assertFalse(w.tags)

    def test_small_csv(self):
        csvinput = io.StringIO("""INV,92,248
P,129,166
P,836,924
QRS,964,1055
T,1055,1339
P,2033,2145
QRS,2181,2270
T,2270,2564
P,3258,3354
QRS,3397,3488
T,3488,3775
P,4477,4578
QRS,4616,4710
T,4710,4995
P,5681,5787
QRS,5829,5919
T,5919,6194
P,7097,7195
QRS,7221,7316,junctional
T,7316,7610
P,8429,8521
QRS,8558,8655
T,8655,8944
P,9767,9846
QRS,9885,9978
T,9978,10266""")
        with stcsv.CSVReader(csvinput) as reader:
            waves = list()
            for data in reader:
                waves.append(data)
            self.assertEqual(len(waves), 26)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()

