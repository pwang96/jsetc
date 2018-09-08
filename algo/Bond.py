from algo.Algo import Algo


class Bond(Algo):
    """

    """

    def find_trades(self):
        sell = self.securities['BOND'].get_sell()
        buy = self.securities['BOND'].get_buy()

        trades = [('BOND', buy + 0.01, 100), ('BOND', sell - 0.01, -100)]

        return trades