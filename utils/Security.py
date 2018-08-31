class Security:
    def __init__(self, symbol, type, members):
        self.symbol = symbol
        self.type = type
        self.members = members

        self.history = []
        self.last_update = None

    def update(self, marketdataupdate):
        self.history.append(marketdataupdate)

    def get_bid(self):
        if self.history:
            last_update = self.history[-1]
            return last_update.bid
        return 0

    def get_ask(self):
        if self.history:
            last_update = self.history[-1]
            return last_update.ask
        return float('inf')

    def get_midprice(self):
        if self.history:
            last_update = self.history[-1]
            return (last_update.bid + last_update.ask) / 2
        return 0
