from algo.Algo import Algo

class ADR(Algo):

    def find_trades(self):
        securities = self.securities

        lowestSell = securities['BABZ'].get_sell()
        highestBuy = securities['BABZ'].get_buy()
        babzPrice = securities['BABZ'].get_midprice()

        ADRlowestSell = securities['BABA'].get_sell()
        ADRhighestBuy = securities['BABA'].get_buy()

        # trades = []

        trades = [('BABA', highestBuy + 1, min(100, 100 - self.positions['BABA'])),
                  ('BABA', lowestSell - 1, max(100, 100 + self.positions['BABA']))]
        # if(highestBuy > ADRhighestBuy and lowestSell < ADRlowestSell):
        #     trades = [('BABA', highestBuy + 1, min(100, 100 - self.positions['BABA'])),
        #               ('BABA', lowestSell - 1, max(100, 100 + self.positions['BABA']))]

        # midBABA = securities['BABA'].get_midprice()
        # midBABZ = securities['BABZ'].get_midprice()


        # converts = []
        #
        #if (ADRlowestSell - highestBuy > 10):
            #buy BABZ at highest buy and convert to ADR, then sell
        #

        # for data in self.market_data:
        #     pass

        return trades
