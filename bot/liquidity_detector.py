class LiquidityDetector:
    def __init__(self, highs, lows):
        self.highs = highs
        self.lows = lows

    def buy_side_liquidity(self):
        liquidity = []
        for i in range(1, len(self.highs)):
            if abs(self.highs[i] - self.highs[i-1]) < 0.5:
                liquidity.append(("BSL", i, self.highs[i]))
        return liquidity

    def sell_side_liquidity(self):
        liquidity = []
        for i in range(1, len(self.lows)):
            if abs(self.lows[i] - self.lows[i-1]) < 0.5:
                liquidity.append(("SSL", i, self.lows[i]))
        return liquidity

    def get_liquidity(self):
        return self.buy_side_liquidity() + self.sell_side_liquidity()
