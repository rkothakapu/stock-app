import pandas as pd
import numpy as np


def update_change(stocks_df: pd.DataFrame):
    assert 'last_price' in stocks_df
    assert 'last_alert_price' in stocks_df
    assert not np.isclose(stocks_df['last_alert_price'], 0.0).any()

    stocks_df['change'] = (stocks_df['last_price'] / stocks_df['last_alert_price']) - 1
