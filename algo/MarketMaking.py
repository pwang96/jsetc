from algo.Algo import Algo
from scipy.stats import linregress

class MarketMaking(Algo):
    """

    """

    def find_trades(self):
        trades = []

        for security in self.securities:
            curr_spread = self.securities[security].get_buy(), self.securities[security].get_sell()
            avg30tick = self.securities[security].average30tick()
            avg = self.securities[security].average()
            stddev = self.securities[security].stddev()
            # if -50 <= self.positions[security] <= 50:
            #     trades.append((security, curr_spread[0] + 1, 20))
            #     trades.append((security, curr_spread[1] - 1, -20))


            # if avg30tick + 1 * stddev < avg:
            #     if -50 <= self.positions[security] <= 50:
            #         trades.append((security, curr_spread[0] + 1, 20))
            #         trades.append((security, curr_spread[1] + 2, -20))
            # elif avg30tick - 1 * stddev > avg:
            #     if -50 <= self.positions[security] <= 50:
            #         trades.append((security, curr_spread[0] - 2, 20))
            #         trades.append((security, curr_spread[1] - 1, -20))
            last10 = self.securities[security].history[-10:]
            m = linregress(list(range(len(last10))), last10)
            print("REGRESSION: {}".format(m))

        return trades
