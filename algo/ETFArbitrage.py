from algo.Algo import Algo


class ETFArbitrage(Algo):
    """
    This algo will check if any ETFs are cheaper/more expensive than the constituent parts
    if ask price of ETF > sum of bid prices of parts + conversion ratio
    if bid price of ETF > sum of ask prices of parts + conversion ratio
    """
    def __init__(self, market_data):
        self.market_data = market_data

    def update_market_data(self, market_data):
        self.market_data = market_data

    def find_trades(self):
        trades = []

        for data in self.market_data:
            pass

        return trades