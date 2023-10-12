"""
Tests for EventSeries Module
----------------------
For further Information see Docstring in test_main.py

:Modul: test_event_series
:Author: Benjamin Gaube
:Date: 2023-10-12
"""

import os
import unittest

import pandas as pd
import numpy as np

from test_main import TestModul
from src.event_series import InterBeatInterval


class TestEventSeriesModul(TestModul):
    def test_constructor(self):
        some_event_series = InterBeatInterval(os.path.join(self.unpacked_directory, r'Data\S1'))
        self.assertNotIsInstance(some_event_series.path, int)
        self.assertIsInstance(some_event_series.final, pd.DataFrame)

    def test__reformat_file(self):
        df = pd.read_csv(os.path.join(self.unpacked_directory, r'Data\S1\Final\IBI.csv'), encoding='utf-8-sig')
        df = InterBeatInterval._reformat_file(df)
        self.assertIsInstance(df.time[0], np.int32)
        self.assertIsInstance(df.interval[77], np.int32)


if __name__ == '__main__':
    unittest.main()
