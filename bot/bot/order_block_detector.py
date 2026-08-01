class OrderBlockDetector:
    def __init__(self):
        pass

    def detect_bullish_ob(self, opens, highs, lows, closes):
        """
        Detect the last bearish candle before a bullish impulse.
        """

        if len(closes) < 2:
            return None

        if closes[-2] < opens[-2] and closes[-1] > highs[-2]:
            return {
                "type": "bullish_order_block",
                "high": highs[-2],
                "low": lows[-2]
            }

        return None

    def detect_bearish_ob(self, opens, highs, lows, closes):
        """
        Detect the last bullish candle before a bearish impulse.
        """

        if len(closes) < 2:
            return None

        if closes[-2] > opens[-2] and closes[-1] < lows[-2]:
            return {
                "type": "bearish_order_block",
                "high": highs[-2],
                "low": lows[-2]
            }

        return None


if __name__ == "__main__":
    opens = [3300, 3315]
    highs = [3310, 3320]
    lows = [3295, 3305]
    closes = [3298, 3322]

    detector = OrderBlockDetector()

    print(detector.detect_bullish_ob(opens, highs, lows, closes))
    print(detector.detect_bearish_ob(opens, highs, lows, closes))
