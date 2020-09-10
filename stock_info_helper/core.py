from yahoo_fin import stock_info as si
from pandas.tseries.offsets import BDay
import pandas_datareader.data as web
from datetime import date, datetime
import pandas as pd


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


def get_prev_eod_df(stocks) -> pd.DataFrame:
    """Read the csv file containing list of stocks.
    Return generic info on these stocks from prev business day"""
    prev_eod_df = get_prev_bday_data(stocks)
    return prev_eod_df


def setup_sod_df(stocks) -> pd.DataFrame:
    """Using prev_eod_df, add new features essential"""
    sod_df = get_prev_eod_df(stocks)
    sod_df['last_price'] = sod_df['Close']
    sod_df['last_alert_price'] = sod_df['Close']

    now = datetime.now()
    sod_df['last_updated_on'] = now
    sod_df['last_updated_on_str'] = now.strftime("%d/%m/%Y %H:%M:%S")
    sod_df['change'] = 0.0

    return sod_df


if __name__ == "__main__":
    df = pd.read_csv('tests/stocks_test.csv')
    gen_data = get_historical_data(df['Stocks'], date.today())
    print("data frame is:\n{}".format(gen_data))
    print("Shape is:\n{}".format(gen_data.shape))

    sod_df = setup_sod_df(df['Stocks'])
    print("data frame is:\n{}".format(sod_df))
    print("Shape is:\n{}".format(sod_df.shape))
