#!/usr/bin/env python3
# coding: utf8

import unittest

if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover('test', pattern='test_*.py')

    test_runner = unittest.TextTestRunner(verbosity=10)
    test_runner.run(test_suite)
