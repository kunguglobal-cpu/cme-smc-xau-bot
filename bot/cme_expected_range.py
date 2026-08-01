class CMEExpectedRange:
    def __init__(self, expected_low, expected_high):
        self.expected_low = expected_low
        self.expected_high = expected_high

    def near_expected_low(self, price, tolerance=1.0):
        return abs(price - self.expected_low) <= tolerance

    def near_expected_high(self, price, tolerance=1.0):
        return abs(price - self.expected_high) <= tolerance

    def bias(self, price):
        if self.near_expected_low(price):
            return "BUY"
        elif self.near_expected_high(price):
            return "SELL"
        else:
            return "NEUTRAL"
