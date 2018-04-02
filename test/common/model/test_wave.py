#!/usr/bin/env python3
# coding: utf8

import unittest

import cardiologs.common.model.wave as wave

class WaveTest(unittest.TestCase):

    def test_getter(self):
        w = wave.Wave(wave.WaveType.INV,
                      wave.WaveTiming(onset=25, offset=100))
        self.assertEqual(w.type, wave.WaveType.INV)
        self.assertEqual(w.timing.onset, 25)
        self.assertEqual(w.timing.offset, 100)
        self.assertFalse(w.tags)
        self.assertIsNotNone(type(w.tags))

        x = wave.Wave(wave.WaveType.P,
                      wave.WaveTiming(onset=25, offset=100),
                      [wave.WaveTags.PREMATURE])
        self.assertEqual(x.type, wave.WaveType.P)
        self.assertEqual(x.timing.onset, 25)
        self.assertEqual(x.timing.offset, 100)
        self.assertTrue(x.tags)
        self.assertIs(type(x.tags), list)
        self.assertEqual(len(x.tags), 1)
        self.assertEqual(x.tags[0], wave.WaveTags.PREMATURE)

if __name__ == '__main__':
    unittest.main()

