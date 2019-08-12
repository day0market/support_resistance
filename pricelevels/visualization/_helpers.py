def _plot_levels(where, levels, only_good=False):
    for l in levels:

        if isinstance(l, float):
            where.axhline(y=l, color='black', linestyle='-')
        elif isinstance(l, dict):
            if 'score' in l.keys():
                if only_good and l['score'] < 0:
                    continue
                color = 'red' if l['score'] < 0 else 'blue'
                where.axhline(y=l['price'], color=color, linestyle='-', linewidth=0.2 * abs(l['score']))
            else:
                where.axhline(y=l['price'], color='black', linestyle='-')
