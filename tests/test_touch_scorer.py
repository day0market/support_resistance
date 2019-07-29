from pricelevels.scoring.touch_scorer import TouchScorer
from tests.fixtures import get_quotes_from_fixture, get_levels_from_fixture


def test_touch_scorer():
    levels = get_levels_from_fixture()
    quotes = get_quotes_from_fixture()
    scorer = TouchScorer()
    scorer.fit(levels, (quotes.iloc[-100:]).copy())

    assert len(levels) == len(scorer.scores)
    scores = scorer.scores

    for level, score in zip(levels, scores):
        assert score[1] == level['price']


if __name__ == '__main__':
    test_touch_scorer()
