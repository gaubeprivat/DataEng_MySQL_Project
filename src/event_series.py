"""
Modul: ibi
Author: Benjamin Gaube
Date: 2023-10-08

providing ibi-object and functionality to process
"""  # TODO

import os

import pandas as pd
import numpy as np
from typing import Generator, Tuple


class InterBeatInterval:

    term_periods = {'final': (1544022000, 1544032800),
                    'mid1': (1539439200, 1539444600),
                    'mid2': (1541862000, 1541867400)}

    def __init__(self, temp_dir):
        self.path = temp_dir
        self.final = self.read_file('Final')
        self.mid1 = self.read_file('Midterm 1')
        self.mid2 = self.read_file('Midterm 2')

    def read_file(self, term: str):  # notation return pandas df
        ibi_df = pd.read_csv(os.path.join(self.path, term, 'IBI.csv'), encoding='utf-8-sig')
        ibi_df = self._reformat_file(ibi_df)
        return ibi_df

    @staticmethod
    def moving_5min_window(ibi_df: pd.DataFrame, term: str) -> Generator[Tuple[int, int, np.array], None, None]:
        """
        Generate 5-minute moving windows of inter-beat interval (IBI) data across a specified term.

        This generator function iterates through the IBI data, providing 5-minute windows,
        shifted in 1-minute steps, within a period specified by the `term` parameter.
        For each yielded window, it provides the central Unix timestamp,
        the count of IBI values within the window, and the IBI values themselves
        in a NumPy array.

        :param ibi_df: pd.DataFrame, containing at least 'time' and 'interval' columns,
            where 'time' should represent Unix timestamps and 'interval' represents IBI values.
        :param term: str, a string to specify the period, depending on the date of the term
            and should be one of {'final', 'mid1', 'mid2'}.
        :return: A generator yielding tuples of (int, int, np.array) representing
            the central timestamp, count of IBI values, and the IBI values in the current window,
            respectively.

        :raise ValueError: Raised if `term` is not one of the allowed options.
        """

        term_options = ['final', 'mid1', 'mid2']
        if term not in term_options:
            raise ValueError(f'The passed string have to be one of the following: {term_options}')

        period = InterBeatInterval.term_periods[term]
        for timestamp in range(period[0], period[1]+1, 60):
            start = timestamp - 150  # minus 2.5min
            stop = timestamp + 150  # plus 2.5min
            window = ibi_df.query('@start <= time <= @stop')

            yield timestamp, len(window), np.array(window.interval)


    @staticmethod
    def _reformat_file(ibi_df: pd.DataFrame) -> pd.DataFrame:
        """
        Reformats a DataFrame of inter-beat interval (IBI) data by adjusting the time column,
        renaming columns, and converting interval data.

        After shifting the time column, the Unix time represents the start time of the interval.
        The intervals are converted into seconds.

        :param ibi_df: pd.DataFrame, the input DataFrame containing IBI data.
        :return: pd.DataFrame, the reformatted DataFrame with adjusted 'time' and 'interval' columns.
        """

        start_time = ibi_df.columns[0]
        ibi_df = ibi_df.rename(columns={start_time: 'time', ' IBI': 'interval'})
        ibi_df.time = ibi_df.time + float(start_time)
        ibi_df.time = ibi_df.time.shift(+1)
        ibi_df.time[0] = ibi_df.time[1] - ibi_df.interval[0]
        ibi_df.interval = (ibi_df.interval * 1000).astype(int)

        return ibi_df
