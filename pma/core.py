from stock_info_helper.core import *


def update_change(stocks_df: pd.DataFrame):
    assert 'last_price' in stocks_df
    assert 'last_alert_price' in stocks_df
    assert not np.isclose(stocks_df['last_alert_price'], 0.0).any()

    stocks_df['change'] = (stocks_df['last_price'] / stocks_df['last_alert_price'].fillna(stocks_df['Close'])) - 1


def get_stocks_to_alert(stocks_df: pd.DataFrame, threshold: float) -> pd.Series:
    assert 'Symbols' in stocks_df

    update_last_price(stocks_df)
    update_change(stocks_df)
    return stocks_df[abs(stocks_df['change']) > threshold][['Symbols', 'change']]


if __name__ == "__main__":
    df_all = setup_sod_df_for_all('tickers_data')
    for key in df_all:
        print(key)
        print("data frame is:\n{}".format(df_all[key]))