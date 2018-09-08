from algo.Algo import Algo


class ETFArbitrage(Algo):
    """
    This algo will check if any ETFs are cheaper/more expensive than the constituent parts
    if ask price of ETF > sum of bid prices of parts + conversion ratio
    if bid price of ETF > sum of ask prices of parts + conversion ratio
    XLK
    3 BOND
    2 AAPL
    3 MSFT
    2 GOOG
    """
    def find_trades(self):
        trades = []
        CONVERSION_FEE = 100
        # only pass in XLF security
        xlf = self.securities['XLK']
        xlf_ask = xlf.get_buy()
        xlf_sell = xlf.get_sell()

        # IF ETF IS UNDERPRICED, BUY ETF, SELL COMPONENTS
        bond_asks = 3 * self.securities['BOND'].get_buy()
        aapl_asks = 2 * self.securities['AAPL'].get_buy()
        msft_asks = 3 * self.securities['MSFT'].get_buy()
        goog_asks = 2 * self.securities['GOOG'].get_buy()
        component_asks = bond_asks + aapl_asks + msft_asks + goog_asks

        bond_sells = 3 * self.securities['BOND'].get_sell()
        aapl_sells = 2 * self.securities['AAPL'].get_sell()
        msft_sells = 3 * self.securities['MSFT'].get_sell()
        goog_sells = 2 * self.securities['GOOG'].get_sell()
        component_sells = bond_sells + aapl_sells + msft_sells + goog_sells

        if xlf_sell > component_asks + CONVERSION_FEE:
            if self.positions['BOND'] >= 3 and \
                self.positions['AAPL'] >= 2 and \
                self.positions['MSFT'] >= 3 and \
                self.positions['GOOG'] >= 2:
                trades.append(('XLK', 'BUY', 10))

        elif component_sells > xlf_ask + CONVERSION_FEE:
            if self.positions['XLK'] >= 10:
                trades.append(('XLK', 'SELL', 10))


        return trades