from Algo import Algo


class ETFArbitrage(Algo):
    def __init__(self, market_data):
        self.market_data = market_data

    def update_market_data(self, market_data):
        self.market_data = market_data

    def find_trades(self):
        trades = []

        for data in self.market_data:
            pass

        return trades