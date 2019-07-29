import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from zigzag import peak_valley_pivots

from .exceptions import InvalidParameterException, InvalidArgumentException


class PriceLevelFromClusters:

    def __init__(self, peak_percent_delta, merge_distance, merge_percent=None, peaks='All',
                 level_selector='median', verbose=False):
        self._peak_percent_delta = peak_percent_delta
        self._merge_distance = merge_distance
        self._merge_percent = merge_percent

        self._level_selector = level_selector
        self._verbose = verbose
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

        pivot_prices = X[indexes]

        return pivot_prices

    def _aggregate_prices_to_levels(self, pivot_prices, distance):
        clustering = AgglomerativeClustering(distance_threshold=distance, n_clusters=None)
        clustering.fit(pivot_prices.reshape(-1, 1))

        df = pd.DataFrame(data=pivot_prices, columns=('price',))
        df['cluster'] = clustering.labels_
        df['peak_count'] = 1

        grouped = df.groupby('cluster').agg(
            {
                'price': self._level_selector,
                'peak_count': 'sum'
            }
        ).reset_index()

        return grouped.to_dict('records')
