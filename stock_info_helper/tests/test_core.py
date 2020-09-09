from unittest import TestCase
from stock_info_helper.core import *
import pandas as pd


class TestCore(TestCase):

    def setUp(self) -> None:
        stocks = pd.read_csv("stocks.csv").iloc[:, 0]
        self.sod_df = setup_sod_df(stocks)
        self.prev_eod_df = get_prev_eod_df(stocks)

    # get_prev_eod_df
    def test_get_prev_eod_df_returnDFWithClosingPrices(self):
        assert ('Close' in self.prev_eod_df)

    # setup_sod_df ##############
    def test_setup_sod_df_returnsDFWithLastPriceFeature(self):
        assert ('last_price' in self.sod_df)

    def test_setup_sod_df_returnsDFWithPriceOnLastAlertFeature(self):
        assert ('price_on_last_alert' in self.sod_df)

    def test_setup_sod_df_returnsDFWithPriceChangePercentFeature(self):
        assert ('price_change_percent' in self.sod_df)
