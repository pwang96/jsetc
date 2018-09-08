import statistics


class Security:
    def __init__(self, symbol, members):
        self.symbol = symbol
        self.members = members

        self.buys = []  # list of lists
        self.sells = []
        self.history = []
        self.last_update = None

    def update(self, buys, sells):
        self.buys = buys
        self.sells = sells
        try:
            self.history.append((buys[0][0] + sells[0][0]) / 2)  # record the midprice
        except Exception:
            print(buys)
            print(sells)

    def average(self):
        return sum(self.history) / len(self.history)

    def average30tick(self):
        return sum(self.history[-30:]) / len(self.history[-30:])

    def stddev(self):
        if len(self.history) > 1:
            return statistics.stdev(self.history)
        elif self.history:
            return self.history[0]
        return 0

    def get_buy(self):
        if self.buys:
            return self.buys[0][0]  # only price, no size
        return 0

    def get_sell(self):
        if self.sells:
            return self.sells[0][0] # only price, no size
        return float('inf')

    def get_midprice(self):
        if self.history:
            return self.history[-1]
        return 0
        
