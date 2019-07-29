import matplotlib.pyplot as plt


def _plot_levels(levels):
    for l in levels:
        if isinstance(l, float):
            plt.axhline(y=l, color='black', linestyle='-')
        elif isinstance(l, dict):
            if 'score' in l.keys():
                color = 'red' if l['score'] < 0 else 'blue'
                plt.axhline(y=l['price'], color=color, linestyle='-', linewidth=0.2 * abs(l['score']))
            else:
                plt.axhline(y=l['price'], color='black', linestyle='-')