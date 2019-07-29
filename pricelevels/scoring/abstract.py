class BaseScorer:

    def fit(self, levels, ohlc_df):
        raise NotImplementedError()