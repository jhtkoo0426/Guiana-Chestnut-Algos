from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

import yahoo_fin.stock_info as si
import requests
import time


class AlpacaAPIConnection():
    """
    Class responsible for connecting to the Alpaca API.
    """

    def __init__(self):
        # Initialize trading client for Alpaca API
        API_KEY         = "PKKL587HXXS43RUJ8SFL"
        SECRET_KEY      = "0mnSWoiLiSQsfUrgwOIMC8YpRQhIZhRSPwADyfR7"
        
        self.client     = TradingClient(api_key=API_KEY, secret_key=SECRET_KEY, paper=True)
        self.account    = self.client.get_account()


    # Account-related details
    def _get_account_status(self):
        return self.account.status

    def _get_account_blocked(self):
        return self.account.account_blocked

    def _get_account_buying_power(self):
        return self.account.buying_power
    
    def _get_account_cash(self):
        return self.account.cash
    
    def _get_account_portfolio_value(self):
        return self.account.portfolio_value
    
    def _get_account_long_market_value(self):
        return self.account.long_market_value
    
    def _get_account_short_market_value(self):
        return self.account.short_market_value
    

    # Market-related functions
    def _get_market_status(self):
        clock = self.client.get_clock()
        return clock.is_open


    # Trading-related functions
    def account_place_buy_order(self, symbol: str, quantity, type='market', time_in_force=TimeInForce.GTC):
        market_order_buy_data = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=OrderSide.BUY,
            type=type,
            time_in_force=time_in_force
        )
        market_order_buy = self.client.submit_order(market_order_buy_data)
    
    def account_place_sell_order(self, symbol: str, quantity, type='market', time_in_force=TimeInForce.GTC):
        market_order_sell_data = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=OrderSide.SELL,
            type=type,
            time_in_force=time_in_force
        )
        market_order_sell = self.client.submit_order(market_order_sell_data)

    def _get_account_holdings(self):
        return self.client.get_all_positions()
    
    def _get_account_position(self, symbol: str):
        positions = self._get_account_holdings()
        for position in positions:
            if position['symbol'].upper() == symbol.upper():
                return position
        return None


class StockScanner(AlpacaAPIConnection):
    """
    Class responsible for processing realtime and historic stock data.
    """

    def __init__(self):
        pass


class Bot(AlpacaAPIConnection):
    """
    Trading bot class to formulate strategies and make market orders.
    """

    def __init__(self):
        super().__init__()
        self.watchlist = []
        self.MAX_VALUE = 500


    def strategy(self):
        self.watchlist = si.tickers_sp500()
        
        while self._get_market_status() is True:
            for ticker in self.watchlist:
                # If have positions, don't buy extra
                if ticker not in self._get_account_holdings().keys():
                    ticker_price = 10
                    self.account_place_buy_order(
                        symbol=ticker,
                        quantity=self.MAX_VALUE//ticker_price
                    )
            time.sleep(1800)

bot     = Bot()
print(bot._get_market_status())