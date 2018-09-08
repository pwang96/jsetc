import select
from gateway.Gateway import Gateway
from algo import ETFArbitrage, Bond

# constants
HOST = 'test-exch-mobrien'
PORT = 25001
TIMEOUT = 0.1
SIDES = ['buy', 'sell']


class Scrooge:
    def __init__(self):
        self.gateway = Gateway()
        self.portfolio = dict()
        self.gateway.connect(HOST, PORT)
        self.algos = [ETFArbitrage.ETFArbitrage(None), Bond.Bond(None)]
        self.sockets = [self.gateway.sock]
        self.market = {}
        self.order_id = 0
        self.handshake = False

    def run(self):
        counter = -1
        while True:
            ready_to_read, _, _ = select.select(self.sockets, [], [], TIMEOUT)
            if ready_to_read:
                counter += 1
                new_market_data = self.gateway.read()
                for md in new_market_data:
                    print(md)
                    self.parse_market_data(md)

            # bond penny pinching
            if counter % 50 == 0:
                for algo in self.algos:
                    algo.update_market_data(self.market)
                    new_trades = algo.find_trades()
                    self.execute_trades(new_trades)


    def parse_market_data(self, market_data):
        type = market_data['type']
        if type == 'hello':
            symbol_positions = market_data['symbols']
            for d in symbol_positions:
                self.portfolio[d['symbol']] = d['position']

            print('current portfolio: ', self.portfolio)
        elif type == 'open':
            pass
        elif type == 'close':
            raise Exception("market closed")
        elif type == 'error':
            print(market_data['error'])
        elif type == 'book':
            symbol = market_data['symbol']
            buys = market_data['buy']
            sells = market_data['sell']
        elif type == 'trade':
            print('trade')
        elif type == 'ack':
            print('ack')
        elif type == 'reject':
            print('reject')
        elif type == 'fill':
            print('fill')
        elif type == 'out':
            print('out')

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
        # trades is a list of tuples of (symbol, price, size)
        for symbol, price, size in trades:
            self.execute_single_trade(symbol, price, size)

    def cancel_obselete_orders(self):
        pass

if __name__ == '__main__':
    scrooge = Scrooge()
    scrooge.run()
