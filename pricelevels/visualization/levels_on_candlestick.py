import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from mpl_finance import candlestick2_ohlc

from ._helpers import _plot_levels


def plot_levels_on_candlestick(df, levels, only_good=False, path=None,
                               formatter=mdates.DateFormatter('%y-%m-%d %H:%M:%S')):
    ohlc = df[['Datetime', 'Open', 'High', 'Low', 'Close']].copy()
    ohlc["Datetime"] = pd.to_datetime(ohlc['Datetime'])
    ohlc["Datetime"] = ohlc["Datetime"].apply(lambda x: mdates.date2num(x))
    f1, ax = plt.subplots(figsize=(10, 5))
    candlestick2_ohlc(ax,
                      closes=ohlc.Close.values,
                      opens=ohlc.Open.values,
                      highs=ohlc.High.values,
                      lows=ohlc.Low.values,
                      colordown='red',
                      colorup='green'
                      )

    _plot_levels(ax, levels, only_good)

    if path:
        plt.savefig(path)
    else:
        plt.show()
    plt.close()
