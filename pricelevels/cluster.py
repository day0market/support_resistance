import pandas as pd
from sklearn.cluster import AgglomerativeClustering

from ._abstract import ZigZagLevels


class PriceLevelFromClusters(ZigZagLevels):

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
