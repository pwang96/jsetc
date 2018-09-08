from algo.Algo import Algo


class MarketMaking(Algo):
    """

    """

    def find_trades(self):
        trades = []

        for security in self.securities:
            curr_spread = self.securities[security].get_buy(), self.securities[security].get_sell()
            midprice = self.securities[security].get_midprice()
            avg = self.securities[security].average()
            stddev = self.securities[security].stddev()
            # if -50 <= self.positions[security] <= 50:
            #     trades.append((security, curr_spread[0] + 1, 20))
            #     trades.append((security, curr_spread[1] - 1, -20))
            if midprice + 2 * stddev < avg:
                if -50 <= self.positions[security] <= 50:
                    trades.append((security, curr_spread[0] + 1, 20))
                    trades.append((security, curr_spread[1] + 1, -20))
            elif midprice - 2 * stddev > avg:
                if -50 <= self.positions[security] <= 50:
                    trades.append((security, curr_spread[0] - 1, 20))
                    trades.append((security, curr_spread[1] - 1, -20))

        return trades
