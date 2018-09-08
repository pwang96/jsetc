from algo.Algo import Algo


class ETFArbitrage(Algo):
    """
    This algo will check if any ETFs are cheaper/more expensive than the constituent parts
    if ask price of ETF > sum of bid prices of parts + conversion ratio
    if bid price of ETF > sum of ask prices of parts + conversion ratio
    3 BOND
    2 AAPL
    3 MSFT
    2 GOOG
    """
    def find_trades(self):
        # only pass in XLF security
        xlf = self.securities['XLF']
        # IF ETF IS UNDERPRICED, BUY ETF, SELL COMPONENTS
        bond_asks = 4 * self.securities['BOND'].get_buy()
        aapl_asks = 2 * self.securities['AAPL'].get_buy()
        msft_asks = 3 * self.securities['MSFT'].get_buy()
        goog_asks = 2 * self.securities['GOOG'].get_buy()

        bond_sells = 4 * self.securities['BOND'].get_sell()
        aapl_sells = 2 * self.securities['AAPL'].get_sell()
        msft_sells = 3 * self.securities['MSFT'].get_sell()
        goog_sells = 2 * self.securities['GOOG'].get_sell()
        trades = []

        for data in self.market_data:
            pass

        return trades