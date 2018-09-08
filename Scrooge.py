import select
from gateway.Gateway import Gateway
from algo import ETFArbitrage

# constants
HOST = 'test-exch-mobrien'
PORT = 25001
TIMEOUT = 0.1
SIDES = ['buy', 'sell']


class Scrooge:
    def __init__(self):
        self.gateway = Gateway()
        self.gateway.connect(HOST, PORT)
        self.algos = [ETFArbitrage.ETFArbitrage(None)]
        self.sockets = [self.gateway.sock]
        self.market = {}
        self.order_id = 0
        self.handshake = False

    def run(self):
        counter = 1
        while True:
            ready_to_read, _, _ = select.select(self.sockets, [], [], TIMEOUT)
            if ready_to_read:
                new_market_data = self.gateway.read()
                self.parse_market_data(new_market_data)
                print(counter, new_market_data)
                counter += 1

            # for algo in self.algos:
            #     algo.update_market_data(self.market)
            #     new_trades = algo.find_trades()

    def parse_market_data(self, market_data):
        type = market_data['type']
        if type == 'hello':
            self.handshake = True
        elif type == 'update':
            self.market = market_data['data']
            print(self.market)

    def execute_single_trade(self, symbol, price, size):
        if size != 0:
            # if size is negative, it's a sell order
            trade = {'type': 'add',
                     'order_id': self.order_id,
                     'symbol': symbol,
                     'dir': SIDES[size < 0],
                     'price': price,
                     'size': abs(size)}

            self.order_id += 1
            # print(trade)

            self.gateway.write(trade)

    def execute_trades(self, trades):
        # trades is a tuple of (symbol, price, size)
        for symbol, price, size in trades:
            self.execute_single_trade(symbol, price, size)

    def cancel_obselete_orders(self):
        pass

if __name__ == '__main__':
    scrooge = Scrooge()
    scrooge.run()
