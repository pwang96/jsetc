import select
from gateway.Gateway import Gateway
from algo import ETFArbitrage

# constants
HOST = 'localhost'
PORT = 42069
TIMEOUT = 0.1


class Scrooge:
    def __init__(self):
        self.gateway = Gateway()
        self.gateway.connect(HOST, PORT)
        self.algos = [ETFArbitrage.ETFArbitrage(None)]
        self.sockets = [self.gateway.sock]
        self.market = {}
        self.order_id = 0

    def run(self):
        while True:
            ready_to_read, _, _ = select.select(self.sockets, [], [], TIMEOUT)
            if ready_to_read:
                new_market_data = self.gateway.read()
                # update self.market with new_market_data

            for algo in self.algos:
                algo.update_market_data(self.market)
                new_trades = algo.find_trades()

    def execute_single_trade(self, symbol, dir, price, size):
        trade = {'type': 'add',
                 'order_id': self.order_id,
                 'symbol': symbol,
                 'dir': dir,
                 'price': price,
                 'size': size}

        self.order_id += 1
        # print(trade)

        self.gateway.write(trade)

    def execute_trades(self, trades):
        # trades is a tuple of (symbol, dir, price, size)
        for symbol, dir, price, size in trades:
            self.execute_single_trade(symbol, dir, price, size)

