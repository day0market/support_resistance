import numpy as np
import pandas as pd
from zigzag import peak_valley_pivots

from .exceptions import InvalidParameterException, InvalidArgumentException


class ZigZagLevels:

    def __init__(self, peak_percent_delta, merge_distance, merge_percent=None, min_bars_between_peaks=0, peaks='All',
                 level_selector='median'):
        self._peak_percent_delta = peak_percent_delta / 100
        self._merge_distance = merge_distance
        self._merge_percent = merge_percent
        self._min_bars_between_peaks = min_bars_between_peaks

        self._level_selector = level_selector
        self._peaks = peaks
        self._levels = None
        self._validate_init_args()

    @property
    def levels(self):
        return self._levels

    def _validate_init_args(self):
        pass

    def fit(self, data):
        if isinstance(data, pd.DataFrame):
            X = data['Close'].values
        elif isinstance(data, np.array):
            X = data
        else:
            raise InvalidArgumentException(
                'Only np.array and pd.DataFrame are supported in `fit` method'
            )

        pivot_prices = self._find_pivot_prices(X)
        levels = self._aggregate_prices_to_levels(pivot_prices, self._get_distance(X))

        self._levels = levels

    def _get_distance(self, X):
        if self._merge_distance:
            return self._merge_distance

        mean_price = np.mean(X)
        return self._merge_percent * mean_price / 100

    def _find_pivot_prices(self, X):
        pivots = peak_valley_pivots(X, self._peak_percent_delta, -self._peak_percent_delta)
        indexes = self._get_pivot_indexes(pivots)
        pivot_prices = X[indexes]

        return pivot_prices

    def _get_pivot_indexes(self, pivots):
        if self._peaks == 'All':
            indexes = np.where(np.abs(pivots) == 1)
        elif self._peaks == 'High':
            indexes = np.where(pivots == 1)
        elif self._peaks == 'Low':
            indexes = np.where(pivots == -1)
        else:
            raise InvalidParameterException(
                'Peaks argument should be one of: `All`, `High`, `Low`'
            )

        return indexes if self._min_bars_between_peaks == 0 else self._filter_by_bars_between(indexes)

    def _filter_by_bars_between(self, indexes):
        indexes = np.sort(indexes).reshape(-1, 1)

        selected = [indexes[0][0]]
        pre_idx = indexes[0][0]
        for i in range(1, len(indexes)):
            if indexes[i][0] - pre_idx < self._min_bars_between_peaks:
                continue
            pre_idx = indexes[i][0]
            selected.append(pre_idx)

        return np.array(selected)

    def _aggregate_prices_to_levels(self, pivot_prices, distance):
        raise NotImplementedError()
