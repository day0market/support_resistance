## PriceLevels

Small package that helps to find support and resistance levels and plot them on chart

![Levels on candlestick chart](candlestick.png?raw=true "Candlestick with levels")


![Levels on zig zag chart](zig_zag.png?raw=true "Zig Zag Price with levels")

## Requirements
* python 3.6+
* matplotlib, pandas, numpy, zigzag, scikit-learn

(For full dependency list check requirements.txt)

## Installation
`python setup.py install`

### How it works?
Algorithm uses AgglomerativeClustering to find levels from pivot points. There are 2 different implementations

* ZigZagClusterLevels
* RawPriceClusterLevels

First one use zigzag pivot points and the second one use all high/low prices 
as pivot points.

Usage example: 

```pl = ZigZagClusterLevels(0.2, 200)
   data = get_quotes_from_fixture()
   pl.fit(data.iloc[-100:])
   levels = pl.levels
```

`fit` method expected to have pandas.DataFrame object with columns `Open, High, Low, Close` or 1d numpy.array of prices 
you want to use to generate levels

#### Please check examples first :)

#### ZigZagClusterLevels

Init args: 
* peak_percent_delta - Min change for new pivot in ZigZag
* merge_distance/merge_percent - Max distance between pivots that can be merged into price level. Comes from AgglomerativeClustering. Only one of those args should be specified, another should be set to None
* min_bars_between_peaks - filter pivots that occurs less than specified number of bars
* peaks (default='All'). Specifies which pivot prices to take. All, High, Low values expected here.
* level_selector(default='median') How to define level from pivots. Options: mean and median



#### RawPriceClusterLevels

Init args:
* merge_distance/merge_percent - Max distance between pivots that can be merged into price level. Comes from AgglomerativeClustering. Only one of those args should be specified, another should be set to None
* level_selector(default='median') How to define level from pivots. Options: mean and median
* use_maximums(default=True) which prices to use.
* bars_for_peak(default=21) take only bars that is high or low across specified number of bars


## other stuff
------

#### Visualization

expected usage:

```
from pricelevels.visualization.levels_on_candlestick import plot_levels_on_candlestick
plot_levels_on_candlestick(df, levels, only_good=False, path=pth)

from pricelevels.visualization.levels_with_zigzag import plot_with_pivots
plot_with_pivots(df['Close'].values, levels, zig_zag_percent)

```


#### Level scoring

Put some score if price touch, cut or pivot near selected levels.
Better levels have higher score. 
It works slowly, so probably you don't want to use it. This idea came from https://stackoverflow.com/questions/8587047/support-resistance-algorithm-technical-analysis

Many parameters, so please check source code.

Usage:
```
from pricelevels.scoring.touch_scorer import TouchScorer
scorer = TouchScorer()
scorer.fit(levels, df.copy())
print(scorer.scores)
```





