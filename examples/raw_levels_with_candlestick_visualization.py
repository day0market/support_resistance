import pandas as pd

from pricelevels.cluster import RawPriceClusterLevels
from pricelevels.visualization.levels_on_candlestick import plot_levels_on_candlestick

df = pd.read_csv('sample.txt')
cl = RawPriceClusterLevels(None, merge_percent=0.25, use_maximums=True, bars_for_peak=91)
cl.fit(df)
levels = cl.levels

plot_levels_on_candlestick(df, levels, only_good=False)  # in case you want to display chart
# plot_levels_on_candlestick(df, levels, only_good=False, path='image.png') # in case you want to save chart to  image
