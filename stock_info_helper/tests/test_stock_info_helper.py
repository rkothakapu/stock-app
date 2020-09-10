import unittest
from stock_info_helper.core import *
import pandas as pd


class Test_stock_info_helper(unittest.TestCase):

    def setUp(self) -> None:
        stocks = pd.read_csv("stocks_test.csv").iloc[:, 0]
        self.num_stocks = len(stocks)
        self.sod_df = setup_sod_df(stocks)
        self.prev_eod_df = get_prev_eod_df(stocks)
        self.generic_df = get_historical_data(stocks, date.today())

    # get_curr_price
    def test_get_curr_price_whenValidTicker_thenReturnsFloat(self):
        valid_ticker = 'AAPL'
        self.assertIsInstance(get_curr_price(valid_ticker), float)

    # get_generic_data
    def test_get_stock_generic_data_returnsPandasSeries(self):
        # generic dataframe contains: ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
        # for each stock
        self.assertEqual(self.generic_df.shape, (self.num_stocks, 6))

    # get_prev_eod_df
    def test_get_prev_eod_df_returnDFWithClosingPrices(self):
        assert ('Close' in self.prev_eod_df)

    # setup_sod_df ##############
    def test_setup_sod_df_returnsDFWithLastPriceFeature(self):
        assert ('last_price' in self.sod_df)

    def test_setup_sod_df_returnsDFWithPriceOnLastAlertFeature(self):
        assert ('last_alert_price' in self.sod_df)

    def test_setup_sod_df_returnsDFWithPriceChangePercentFeature(self):
        assert ('change' in self.sod_df)
