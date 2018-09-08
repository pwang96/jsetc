class Security:
    def __init__(self, symbol, members):
        self.symbol = symbol
        self.members = members

        self.buys = []
        self.sells = []
        self.history = []
        self.last_update = None

    def update(self, buys, sells):
        self.buys = buys
        self.sells = sells
        self.history.append((buys[0] + sells[0])/2)  # record the midprice

    def get_buy(self):
        if self.buys:
            return self.buys[0]
        return 0

    def get_sell(self):
        if self.sells:
            return self.sells[0]
        return float('inf')

    def get_midprice(self):
        if self.history:
            last_update = self.history[-1]
            return (last_update.bid + last_update.ask) / 2
        return 0
        
