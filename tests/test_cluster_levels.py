import numpy as np

from pricelevels.cluster import ZigZagClusterLevels
from tests.fixtures import get_quotes_from_fixture


def test_find_pivot_prices():
    pl = ZigZagClusterLevels(0.2, 200)

    data = get_quotes_from_fixture()
    closes = data['Close'].values

    pivot_prices = pl._find_potential_level_prices(closes[-100:])

    expected = np.array([136940, 135750, 136510, 135540, 136920, 135370, 135890, 135340, 136690,
                         134800, 135070, 134720, 135370, 134180, 135370, 134660, 135340, 134020])

    assert (pivot_prices == expected).all()


def test_price_level_from_clusters_fit():
    pl = ZigZagClusterLevels(0.2, 200)

    data = get_quotes_from_fixture()

    pl.fit(data.iloc[-100:])

    assert len(pl.levels) > 0
    assert isinstance(pl.levels, list)

    for i in range(1, len(pl.levels)):
        assert abs(pl.levels[i]['price'] - pl.levels[i - 1]['price']) > 200


if __name__ == '__main__':
    test_find_pivot_prices()
    test_price_level_from_clusters_fit()
