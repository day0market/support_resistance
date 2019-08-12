import pandas as pd
from sklearn.cluster import AgglomerativeClustering

from ._abstract import BaseZigZagLevels, BaseLevelFinder


def _cluster_prices_to_levels(prices, distance, level_selector='mean'):
    clustering = AgglomerativeClustering(distance_threshold=distance, n_clusters=None)
    try:
        clustering.fit(prices.reshape(-1, 1))
    except ValueError:
        return None

    df = pd.DataFrame(data=prices, columns=('price',))
    df['cluster'] = clustering.labels_
    df['peak_count'] = 1

    grouped = df.groupby('cluster').agg(
        {
            'price': level_selector,
            'peak_count': 'sum'
        }
    ).reset_index()

    return grouped.to_dict('records')


class ZigZagClusterLevels(BaseZigZagLevels):

    def _aggregate_prices_to_levels(self, prices, distance):
        return _cluster_prices_to_levels(prices, distance, self._level_selector)


class RawPriceClusterLevels(BaseLevelFinder):
    def __init__(self, merge_distance, merge_percent=None, level_selector='median', use_maximums=True,
                 bars_for_peak=21):

        self._use_max = use_maximums
        self._bars_for_peak = bars_for_peak
        super().__init__(merge_distance, merge_percent, level_selector)

    def _validate_init_args(self):
        super()._validate_init_args()
        if self._bars_for_peak % 2 == 0:
            raise Exception('N bars to define peak should be odd number')

    def _find_potential_level_prices(self, X):
        d = pd.DataFrame(data=X, columns=('price',))
        bars_to_shift = int((self._bars_for_peak - 1) / 2)

        if self._use_max:
            d['F'] = d['price'].rolling(window=self._bars_for_peak).max().shift(-bars_to_shift)
        else:
            d['F'] = d['price'].rolling(window=self._bars_for_peak).min().shift(-bars_to_shift)

        prices = pd.unique(d[d['F'] == d['price']]['price'])

        return prices

    def _aggregate_prices_to_levels(self, prices, distance):
        return _cluster_prices_to_levels(prices, distance, self._level_selector)
