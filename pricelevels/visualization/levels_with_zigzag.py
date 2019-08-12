import matplotlib.pyplot as plt
import numpy as np
from zigzag import peak_valley_pivots

from ._helpers import _plot_levels


def plot_with_pivots(X, levels, zigzag_percent=1, only_good=False, path=None):
    pivots = peak_valley_pivots(X, zigzag_percent / 100, -zigzag_percent / 100)
    plt.xlim(0, len(X))
    plt.ylim(X.min() * 0.995, X.max() * 1.005)
    plt.plot(np.arange(len(X)), X, 'k-', alpha=0.9)
    plt.plot(np.arange(len(X))[pivots != 0], X[pivots != 0], 'k:', alpha=0.5)

    plt.scatter(np.arange(len(X))[pivots == 1], X[pivots == 1], color='g')
    plt.scatter(np.arange(len(X))[pivots == -1], X[pivots == -1], color='r')

    _plot_levels(plt, levels, only_good)
    if path:
        plt.savefig(path)
    else:
        plt.show()
    plt.close()
