class Algo:
    def __init__(self, securities, positions):
        self.securities = securities
        self.positions = positions

    def update_market_data(self, securities, positions):
        self.securities = securities
        self.positions = positions

    def find_trades(self):
        return []