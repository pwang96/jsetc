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
        print(self.positions)
        conversions = []
        trades = []
        CONVERSION_FEE = 100
        # only pass in XLF security
        xlf = self.securities['XLK']
        xlf_bid = xlf.get_buy()
        xlf_ask = xlf.get_sell()

        # IF ETF IS UNDERPRICED, BUY ETF, SELL COMPONENTS
        bond_bids = 3 * self.securities['BOND'].get_buy()
        aapl_bids = 2 * self.securities['AAPL'].get_buy()
        msft_bids = 3 * self.securities['MSFT'].get_buy()
        goog_bids = 2 * self.securities['GOOG'].get_buy()
        component_bids = bond_bids + aapl_bids + msft_bids + goog_bids

        bond_asks = 3 * self.securities['BOND'].get_sell()
        aapl_asks = 2 * self.securities['AAPL'].get_sell()
        msft_asks = 3 * self.securities['MSFT'].get_sell()
        goog_asks = 2 * self.securities['GOOG'].get_sell()
        component_asks = bond_asks + aapl_asks + msft_asks + goog_asks


        for multiple in range(1, 6):
            if component_asks + CONVERSION_FEE//multiple < xlf_bid:
                if self.positions['BOND'] >= 3*multiple and \
                    self.positions['AAPL'] >= 2*multiple and \
                    self.positions['MSFT'] >= 3*multiple and \
                    self.positions['GOOG'] >= 2*multiple:
                    conversions.append(('XLK', 'BUY', 10*multiple))
                    trades.append(('XLK', xlf_bid, -10*multiple))

            elif xlf_ask + CONVERSION_FEE//multiple < component_bids:
                if self.positions['XLK'] >= 10*multiple:
                    conversions.append(('XLK', 'SELL', 10*multiple))
                    trades.append(('BOND', bond_bids, -3*multiple))
                    trades.append(('AAPL', aapl_bids, -2*multiple))
                    trades.append(('MSFT', msft_bids, -3*multiple))
                    trades.append(('GOOG', goog_bids, -2*multiple))

        return conversions, trades