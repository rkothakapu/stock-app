from yahoo_fin import stock_info as si
from pandas.tseries.offsets import BDay
import pandas_datareader.data as web
from datetime import date, datetime
import pandas as pd


def get_curr_price(ticker: str) -> float:
    """Retrieves the current price for a requested ticker symbol"""
    try:
        return si.get_live_price(ticker)
    except Exception as e:
        print(e)


def get_stock_generic_data(ticker: pd.Series, day: date) -> pd.DataFrame:
    """Get info on a stock for a given day
    Information retrieved: High, low, open, close, volume, Adj Close
    """
    return web.DataReader(ticker, 'yahoo', day, day)


def get_prev_bday_data(ticker: pd.Series) -> pd.DataFrame:
    """Retrieve info for previous business day"""
    today = date.today()
    prev_bday = today - BDay(1)
    return get_stock_generic_data(ticker, prev_bday)


def get_prev_eod_df(stocks) -> pd.DataFrame:
    """Read the csv file containing list of stocks.
    Return generic info on these stocks from prev business day"""
    prev_eod_df = get_prev_bday_data(stocks)
    return prev_eod_df.stack()


def setup_sod_df(stocks) -> pd.DataFrame:
    """Using prev_eod_df, add new features essential"""
    sod_df = get_prev_eod_df(stocks)
    sod_df['last_price'] = sod_df['Close']
    sod_df['price_on_last_alert'] = sod_df['Close']

    now = datetime.now()
    sod_df['last_updated_on'] = now
    sod_df['last_updated_on_str'] = now.strftime("%d/%m/%Y %H:%M:%S")
    sod_df['price_change_percent'] = 0.0

    return sod_df
