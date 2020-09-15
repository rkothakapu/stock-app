import unittest
from pma.core import *
import numpy as np


class TestPMA(unittest.TestCase):
    def setUp(self) -> None:
        self.stocks_df = pd.DataFrame({
            'Symbols': ['FB', 'AAPL', 'MSFT', 'NFLX', 'GOOGL', 'RAND'],
            'last_price': [103.5, 97, 107.5, 93.2, 100.0, 0.2],
            'last_alert_price': [100.0, 100.0, 100.0, 100.0, 100.0, 0.1],
            'Close': [100.0, 100.0, 100.0, 100.0, 100.0, 0.1]
        })

    def test_update_change(self):
        expected_change = pd.Series([0.035, -0.03, 0.075, -0.068, 0.0, 1.0])
        update_change(stocks_df=self.stocks_df)
        self.assertTrue(np.allclose(expected_change, self.stocks_df['change']))

    def test_get_stocks_to_alert(self):
        expected_top_movers = ['MSFT', 'NFLX', 'RAND']
        update_change(self.stocks_df)
        top_movers_df = get_stocks_to_alert(self.stocks_df, 0.05)
        # Validate 'MSFT' and 'NFLX' are detected as top movers
        assert expected_top_movers in top_movers_df['Symbols'].unique()