"""
Modul: test_event_series
Author: Benjamin Gaube
Date: 2023-10-08
"""  # TODO

import os
import unittest

import pandas as pd

from test_main import TestModul
from src.event_series import InterBeatInterval


class TestEventSeriesModul(TestModul):
    def test_constructor(self):
        some_event_series = InterBeatInterval(os.path.join(self.unpacked_directory, r'Data\S1'))
        self.assertNotIsInstance(some_event_series.path, int)
        self.assertIsInstance(some_event_series.final, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
