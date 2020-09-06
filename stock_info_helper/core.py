from yahoo_fin import stock_info as si


def get_curr_price(ticker):
    """Retrieves the current price for a requested ticker symbol"""
    return si.get_live_price(ticker)
