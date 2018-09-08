from algo.Algo import Algo

class ADR(Algo):

    def find_trades(self):
        securities = self.securities

        lowestSell = securities['BABZ'].get_sell()
        highestBuy = securities['BABZ'].get_buy()
        babzPrice = securities['BABZ'].get_midprice()

        ADRlowestSell = securities['BABA'].get_sell()
        ADRhighestBuy = securities['BABA'].get_buy()

        trades = []

        if(highestBuy > ADRhighestBuy and lowestSell < ADRlowestSell):
            trades = [('BABA', highestBuy + 0.01, 100), ('BABA', lowestSell - 0.01, -100)]

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
