import numpy as np

from ._abstract import ZigZagLevels


class CounterLevels(ZigZagLevels):

    def __init__(self, min_bars_between_peaks, peak_percent_delta, merge_distance, merge_percent=None, peaks='All',
                 level_selector='median', verbose=False):
        super().__init__(peak_percent_delta, merge_distance, merge_percent, peaks,
                         level_selector, verbose)



    def _get_pivot_indexes(self, pivots):
        indexes = super()._get_pivot_indexes(pivots)
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
        levels = sorted(pivot_prices)
        scored_levels = []
        for price_level in levels:
            count = 0
            for other_level in levels:
                if other_level < price_level - distance:
                    continue
                if other_level > price_level + distance:
                    break
                count += 1

            scored_levels.append(
                {
                    'price': price_level,
                    'count': count
                }
            )

        return scored_levels
