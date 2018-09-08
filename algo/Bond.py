from algo.Algo import Algo


class Bond(Algo):
    """

    """

    def find_trades(self):
        sell = self.securities['BOND'].get_sell()
        buy = self.securities['BOND'].get_buy()

        trades = [('BOND', min(1000, buy + 1), 100), ('BOND', sell - 1, -100)]

        return trades