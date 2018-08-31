class MarketDataUpdate:
    def __init__(self, symbol, bid, ask, bid_size, ask_size, last_sale, last_size):
        self.symbol = symbol
        self.bid = bid
        self.ask = ask
        self.bid_size = bid_size
        self.ask_size = ask_size
        self.last_sale = last_sale
        self.last_size = last_size