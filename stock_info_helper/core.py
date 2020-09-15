from yahoo_fin import stock_info as si
from pandas.tseries.offsets import BDay
import pandas_datareader.data as web
from datetime import date, datetime
import pandas as pd
import numpy as np
import os


def get_curr_price(ticker: str) -> float:
    """Retrieves the current price for a requested ticker symbol
    Can call the function with a list of tickers or
    pandas Series containing ticker symbols as well.
    """
    try:
        return si.get_live_price(ticker)
    except Exception as e:
        print(e)


def get_historical_data(stocks: pd.Series, day: date) -> pd.DataFrame:
    """Get info on a stock for a given day
    Information retrieved: High, low, open, close, volume, Adj Close
    """
    return pd.DataFrame(web.DataReader(stocks, 'yahoo', day, day).iloc[0]).unstack(level=0).droplevel(level=0, axis=1)


def get_prev_bday_data(stocks: pd.Series) -> pd.DataFrame:
    """Retrieve info for previous business day"""
    today = date.today()
    prev_bday = today - BDay(1)
    return get_historical_data(stocks, prev_bday)


def update_last_price(stocks_df: pd.DataFrame):
    """Retrieve the current stock price and update the dataframe
    This method doesn't update last_updated and last_updated_str features
    Calling function must update them"""
    stocks_df['last_price'] = stocks_df['Symbols'].apply(get_curr_price())


def setup_sod_df(stocks) -> pd.DataFrame:
    """Using get_prev_bday_data, add new features essential"""
    sod_df = get_prev_bday_data(stocks)
    sod_df['last_price'] = np.nan
    sod_df['last_alert_price'] = np.nan

    now = datetime.now()
    sod_df['last_updated'] = now
    sod_df['last_updated_str'] = now.strftime("%d/%m/%Y %H:%M:%S")
    sod_df['change'] = 0.0

    return sod_df


def setup_sod_df_for_all(directory):
    """Filepath contains list of csv files containing ticker symbols.
    Setup sod df for each"""
    df_all = {}
    for filename in os.listdir(os.path.join(os.getcwd(), directory)):
        if filename.endswith(".csv"):
            file = os.path.join(directory, filename)
            ticker_df = pd.read_csv(file)
            df_all[file] = setup_sod_df(ticker_df['Stocks'])

    return df_all


if __name__ == "__main__":
    df = pd.read_csv('tests/stocks_test.csv')
    gen_data = get_historical_data(df['Stocks'], date.today())
    print("data frame is:\n{}".format(gen_data))
    print("Shape is:\n{}".format(gen_data.shape))

    sod_df_test = setup_sod_df(df['Stocks'])
    print("data frame is:\n{}".format(sod_df_test))
    print("Shape is:\n{}".format(sod_df_test.shape))

    print("Current prices are is:\n{}".format(df['Stocks'].apply(get_curr_price)))
