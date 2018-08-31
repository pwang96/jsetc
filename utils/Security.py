class Security:
    def __init__(self, symbol, type, members, bids, asks):
        self.symbol = symbol
        self.type = type
        self.members = members
        self.bids = bids
        self.asks = asks

        self.historical_prices = []

    def update(self, bids, asks):
        self.bids = bids
        self.asks = asks
        