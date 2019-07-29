from pricelevels.scoring.touch_scorer import TouchScorer
from pricelevels.visualization.levels_with_zigzag import plot_with_pivots
from tests.fixtures import get_levels_from_fixture, get_quotes_from_fixture


def check_zigzag():
    levels = get_levels_from_fixture()
    quotes = get_quotes_from_fixture().iloc[-100:]
    scoring = TouchScorer()
    scoring.fit(levels, quotes)

    plot_with_pivots(quotes.Close.values, levels, zigzag_percent=0.2)

    for level, score in zip(levels, scoring.scores):
        level['score'] = score[-1].score

    plot_with_pivots(quotes.Close.values, levels, zigzag_percent=0.2)


if __name__ == '__main__':
    check_zigzag()
