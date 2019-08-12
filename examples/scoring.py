import pandas as pd

from pricelevels.cluster import RawPriceClusterLevels
from pricelevels.scoring.touch_scorer import TouchScorer

df = pd.read_csv('sample.txt')
cl = RawPriceClusterLevels(None, merge_percent=0.25, use_maximums=True, bars_for_peak=91)
cl.fit(df)
levels = cl.levels
scorer = TouchScorer()
scorer.fit(levels, df.copy())

print(scorer.scores)
