class LiquiditySweepDetector:
    def __init__(self):
        pass

    def detect_buy_side_sweep(self, highs, closes):
        """
        Detect a buy-side liquidity sweep.
        Price takes the previous high but closes back below it.
        """

        if len(highs) < 2 or len(closes) < 1:
            return None

        previous_high = highs[-2]

        if highs[-1] > previous_high and closes[-1] < previous_high:
            return {
                "type": "buy_side_sweep",
                "level": previous_high
            }

        return None

    def detect_sell_side_sweep(self, lows, closes):
        """
        Detect a sell-side liquidity sweep.
        Price takes the previous low but closes back above it.
        """

        if len(lows) < 2 or len(closes) < 1:
            return None

        previous_low = lows[-2]

        if lows[-1] < previous_low and closes[-1] > previous_low:
            return {
                "type": "sell_side_sweep",
                "level": previous_low
            }

        return None


if __name__ == "__main__":
    highs = [3320, 3335]
    lows = [3290, 3280]
    closes = [3310, 3318]

    detector = LiquiditySweepDetector()

    print(detector.detect_buy_side_sweep(highs, closes))
    print(detector.detect_sell_side_sweep(lows, closes))
