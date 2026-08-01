# bot/market_structure.py

class MarketStructure:
    def __init__(self):
        self.trend = "UNKNOWN"

    def detect_trend(self, current_high, previous_high, current_low, previous_low):
        if current_high > previous_high and current_low > previous_low:
            self.trend = "BULLISH"
        elif current_high < previous_high and current_low < previous_low:
            self.trend = "BEARISH"
        else:
            self.trend = "RANGING"

        return self.trend


if __name__ == "__main__":
    ms = MarketStructure()
    trend = ms.detect_trend(
        current_high=3360,
        previous_high=3350,
        current_low=3330,
        previous_low=3320
    )
    print(trend)
