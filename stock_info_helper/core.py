from yahoo_fin import stock_info as si
from pandas.tseries.offsets import BDay
import pandas_datareader.data as web
from datetime import date
import pandas as pd


def get_curr_price(ticker: str) -> float:
    """Retrieves the current price for a requested ticker symbol"""
    try:
        return si.get_live_price(ticker)
    except Exception as e:
        print(e)


def get_stock_generic_data(ticker: str, day: date) -> pd.DataFrame:
    """Get info on a stock for a given day
    Information retrieved: High, low, open, close, volume, Adj Close
    """
    return web.DataReader(ticker, 'yahoo', day, day)


def get_prev_bday_data(ticker: str) -> pd.DataFrame:
    """Retrieve info for previous business day"""
    today = date.today()
    prev_bday = today - BDay(1)
    return get_stock_generic_data(ticker, prev_bday)
