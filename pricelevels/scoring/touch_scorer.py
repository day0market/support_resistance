from enum import Enum, auto

import numpy as np

from .abstract import BaseScorer


class PointEventType(Enum):
    CUT_BODY = auto()
    CUT_WICK = auto()
    TOUCH_DOWN_HIGHLOW = auto()
    TOUCH_DOWN = auto()
    TOUCH_UP_HIGHLOW = auto()
    TOUCH_UP = auto()


class PointEvent:
    def __init__(self, event_type, timestamp, score_change):
        self.type = event_type
        self.timestamp = timestamp
        self.score_change = score_change


class PointScore:

    def __init__(self, point, score, point_event_list):
        self.point = point
        self.score = score
        self.point_event_list = point_event_list

    def __str__(self):
        return f'| price: {self.point}: score{self.score} |'

    def __repr__(self):
        return str(self)


class TouchScorer(BaseScorer):

    def __init__(self, min_candles_between_body_cuts=5, diff_perc_from_extreme=0.05,
                 min_distance_between_levels=0.1, min_trend_percent=0.5, diff_perc_for_candle_close=0.05,
                 score_for_cut_body=-2, score_for_cut_wick=-1, score_for_touch_high_low=1, score_for_touch_normal=2):

        self.DIFF_PERC_FOR_CANDLE_CLOSE = diff_perc_for_candle_close
        self.MIN_DIFF_FOR_CONSECUTIVE_CUT = min_candles_between_body_cuts
        self.DIFF_PERC_FROM_EXTREME = diff_perc_from_extreme
        self.DIFF_PERC_FOR_INTRASR_DISTANCE = min_distance_between_levels
        self.MIN_PERC_FOR_TREND = min_trend_percent

        self.score_for_cut_body = score_for_cut_body
        self.score_for_cut_wick = score_for_cut_wick
        self.score_for_touch_high_low = score_for_touch_high_low
        self.score_for_touch_normal = score_for_touch_normal

        self._scores = None

    def closeFromExtreme(self, key, min_value, max_value):
        return abs(key - min_value) < (min_value * self.DIFF_PERC_FROM_EXTREME / 100.0) or \
               abs(key - max_value) < (max_value * self.DIFF_PERC_FROM_EXTREME / 100)

    @staticmethod
    def getMin(candles):
        return candles['Low'].min()

    @staticmethod
    def getMax(candles):
        return candles['High'].max()

    def similar(self, key, used):
        for value in used:
            if abs(key - value) <= (self.DIFF_PERC_FOR_INTRASR_DISTANCE * value / 100):
                return True
        return False

    def fit(self, levels, ohlc_df):
        scores = []
        high_low_list = self._get_high_low_list(ohlc_df)

        for i, obj in enumerate(levels):
            if isinstance(obj, float):
                price = obj
            elif isinstance(obj, dict):
                try:
                    price = obj['price']
                except KeyError:
                    raise Exception('`levels` supposed to be a list of floats or list of dicts with `price` key')
            else:
                raise Exception('`levels` supposed to be a list of floats or list of dicts with `price` key')

            score = self._get_level_score(ohlc_df, high_low_list, price)
            scores.append((i, price, score))

        self._scores = scores

    @property
    def scores(self):
        return self._scores

    @staticmethod
    def _get_high_low_list(ohlc_df):
        rolling_lows = ohlc_df['Low'].rolling(window=3).min().shift(-1)
        rolling_highs = ohlc_df['High'].rolling(window=3).min().shift(-1)
        high_low_list = np.where(ohlc_df['Low'] == rolling_lows, True, False)
        high_low_list = np.where(ohlc_df['High'] == rolling_highs, True, high_low_list)

        return high_low_list.tolist()

    def _get_level_score(self, candles, high_low_marks, price):
        events = []
        score = 0.0
        last_cut_pos = -10
        for i in range(len(candles)):
            candle = candles.iloc[i]
            # If the body of the candle cuts through the price, then deduct some score
            if self.cut_body(price, candle) and i - last_cut_pos > self.MIN_DIFF_FOR_CONSECUTIVE_CUT:
                score += self.score_for_cut_body
                last_cut_pos = i
                events.append(PointEvent(PointEventType.CUT_BODY, candle['Datetime'], self.score_for_cut_body))
            # If the wick of the candle cuts through the price, then deduct some score
            elif self.cut_wick(price, candle) and (i - last_cut_pos > self.MIN_DIFF_FOR_CONSECUTIVE_CUT):
                score += self.score_for_cut_wick
                last_cut_pos = i
                events.append(PointEvent(PointEventType.CUT_WICK, candle['Datetime'], self.score_for_cut_body))
            # If the if is close the high of some candle and it was in an uptrend, then add some score to this
            elif self.touch_high(price, candle) and self.in_up_trend(candles, price, i):
                high_low_value = high_low_marks[i]
                # If it is a high, then add some score S1
                if high_low_value:
                    score += self.score_for_touch_high_low
                    events.append(
                        PointEvent(PointEventType.TOUCH_UP_HIGHLOW, candle['Datetime'], self.score_for_touch_high_low))
                # Else add S2. S2 > S1
                else:
                    score += self.score_for_touch_normal
                    events.append(PointEvent(PointEventType.TOUCH_UP, candle['Datetime'], self.score_for_touch_normal))

            # If the if is close the low of some candle and it was in an downtrend, then add some score to this
            elif self.touch_low(price, candle) and self.in_down_trend(candles, price, i):
                high_low_value = high_low_marks[i]
                # If it is a high, then add some score S1
                if high_low_value is not None and not high_low_value:
                    score += self.score_for_touch_high_low
                    events.append(
                        PointEvent(PointEventType.TOUCH_DOWN, candle['Datetime'], self.score_for_touch_high_low))
                # Else add S2. S2 > S1
                else:
                    score += self.score_for_touch_normal
                    events.append(
                        PointEvent(PointEventType.TOUCH_DOWN_HIGHLOW, candle['Datetime'], self.score_for_touch_normal))

        return PointScore(price, score, events)

    def in_down_trend(self, candles, price, start_pos):
        # Either move #MIN_PERC_FOR_TREND in direction of trend, or cut through the price
        pos = start_pos
        while pos >= 0:
            if candles['Low'].iat[pos] < price:
                return False
            if candles['Low'].iat[pos] - price > (price * self.MIN_PERC_FOR_TREND / 100):
                return True
            pos -= 1

        return False

    def in_up_trend(self, candles, price, start_pos):
        pos = start_pos
        while pos >= 0:
            if candles['High'].iat[pos] > price:
                return False
            if price - candles['Low'].iat[pos] > (price * self.MIN_PERC_FOR_TREND / 100):
                return True
            pos -= 1

        return False

    def touch_high(self, price, candle):
        high = candle['High']
        ltp = candle['Close']
        return high <= price and abs(high - price) < ltp * self.DIFF_PERC_FOR_CANDLE_CLOSE / 100

    def touch_low(self, price, candle):
        low = candle['Low']
        ltp = candle['Close']
        return low >= price and abs(low - price) < ltp * self.DIFF_PERC_FOR_CANDLE_CLOSE / 100

    def cut_body(self, point, candle):
        return max(candle['Open'], candle['Close']) > point and min(candle['Open'], candle['Close']) < point

    def cut_wick(self, price, candle):
        return not self.cut_body(price, candle) and candle['High'] > price and candle['Low'] < price
