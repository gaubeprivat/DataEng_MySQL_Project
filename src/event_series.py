"""
Modul: ibi
Author: Benjamin Gaube
Date: 2023-10-08

providing ibi-object and functionality to process
"""  # TODO

import os

import pandas as pd


class InterBeatInterval:
    def __init__(self, temp_dir):
        self.path = temp_dir
        self.final = self.read_file('Final')
        self.mid1 = self.read_file('Midterm 1')
        self.mid2 = self.read_file('Midterm 2')

    def _reformat_file(self, ibi_df):
        pass  # TODO: organize time and columnames and so on
        return ibi_df

    def read_file(self, term: str):  # notation return pandas df
        ibi_df = pd.read_csv(os.path.join(self.path, term, 'IBI.csv'), encoding='utf-8-sig')
        ibi_df = self._reformat_file(ibi_df)
        return ibi_df

    def moving_5min_window(self, ibi_df):
        # TODO: have to be a generator. Yielding based on ibi_df 5min-windows on the event-series
        pass
