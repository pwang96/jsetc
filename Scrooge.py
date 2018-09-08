import select
from gateway.Gateway import Gateway
from algo import ETFArbitrage, Bond, MarketMaking, ADR
from utils.Security import Security

# constants
HOST = 'test-exch-mobrien'
# HOST = 'production'
PORT = 25000
TIMEOUT = 0.1
SIDES = ['BUY', 'SELL']
SECURITIES = ['BOND', 'MSFT', 'AAPL', 'GOOG', 'XLK', 'BABA', 'BABZ']
SEC_MEMBERS = [[], [], [], [], ['BOND', 'AAPL', 'MSFT', 'GOOG'], [], []]

class Scrooge:
    def __init__(self):
        self.gateway = Gateway()
        self.portfolio = dict()
        self.gateway.connect(HOST, PORT)
        self.sockets = [self.gateway.sock]
        self.market = {}
        self.order_id = 0
        self.securities = [Security(sec, mem) for sec, mem in zip(SECURITIES, SEC_MEMBERS)]
        self.security_map = {sec.symbol: sec for sec in self.securities}
        self.algos = [ETFArbitrage.ETFArbitrage(self.security_map, self.portfolio),
                      Bond.Bond(self.security_map, self.portfolio),
                      MarketMaking.MarketMaking(self.security_map, self.portfolio),
                      ADR.ADR(self.security_map, self.portfolio)]

        self.num_updates = 0

    def run(self):
        counter = -1
        while True:
            ready_to_read, _, _ = select.select(self.sockets, [], [], TIMEOUT)
            if ready_to_read:
                counter += 1
                self.num_updates += 1
                new_market_data = self.gateway.read()
                for md in new_market_data:
                    self.parse_market_data(md)

            if counter % 50 == 0:
                for algo in self.algos:
                    algo.update_market_data(self.security_map, self.portfolio)
                    new_trades = algo.find_trades()
                    for symbol, price, size in new_trades:
                        if -100 <= self.portfolio[symbol] + size <= 100:
                            if self.portfolio['USD'] < -15000:
                                if size > 0:
                                    continue
                            self.execute_single_trade(symbol, price, size)

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
            self.security_map[symbol].update(buys, sells)
        elif type == 'trade':
            print('trade')
        elif type == 'ack':
            print('ack')
        elif type == 'reject':
            print('order number {} rejected because of {}'.format(str(market_data['order_id']), market_data['error']))
        elif type == 'fill':
            print('order number {} filled'.format(str(market_data['order_id'])))
        elif type == 'out':
            print('order number {} out'.format(str(market_data['order_id'])))

    def execute_single_trade(self, symbol, price, size):
        if size != 0 and -100 <= self.portfolio[symbol] + size <= 100:
            # if size is negative, it's a sell order
            trade = {'type': 'add',
                     'order_id': self.order_id,
                     'symbol': symbol,
                     'dir': SIDES[size < 0],
                     'price': price,
                     'size': abs(size)}


            self.portfolio[symbol] += size
            self.portfolio['USD'] -= size * price

            print("executed trade number {}: {}".format(str(self.order_id), str(trade)))
            self.order_id += 1
            self.gateway.write(trade)

    def execute_convert(self, symbol, dir, size):
        trade = {"type": "convert",
                 "order_id": self.order_id,
                 "symbol": symbol,
                 "dir": dir,
                 "size": size}

        print("executed conversion number {}: {}".format(str(self.order_id), str(trade)))
        self.order_id += 1
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
