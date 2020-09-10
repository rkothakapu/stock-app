import unittest
from pma.core import *
import numpy as np


class TestPMA(unittest.TestCase):
    def setUp(self) -> None:
        self.stocks_df = pd.DataFrame({
            'Symbols': ['FB', 'AAPL', 'MSFT', 'NFLX', 'GOOGL', 'RAND'],
            'last_price': [103.5, 97, 107.5, 93.2, 100.0, 0.2],
            'last_alert_price': [100.0, 100.0, 100.0, 100.0, 100.0, 0.1]
        })

    def test_update_change(self):
        expected_change = pd.Series([0.035, -0.03, 0.075, -0.068, 0.0, 1.0])
        update_change(stocks_df=self.stocks_df)
        self.assertTrue(np.allclose(expected_change, self.stocks_df['change']))


