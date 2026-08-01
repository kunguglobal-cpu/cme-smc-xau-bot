class FairValueGapDetector:
    def __init__(self):
        pass

    def detect_bullish_fvg(self, candles):
        """
        Bullish FVG:
        Candle 1 high < Candle 3 low
        """
        gaps = []

        for i in range(len(candles) - 2):
            c1 = candles[i]
            c3 = candles[i + 2]

            if c1["high"] < c3["low"]:
                gaps.append({
                    "type": "bullish",
                    "start": c1["high"],
                    "end": c3["low"],
                    "index": i
                })

        return gaps

    def detect_bearish_fvg(self, candles):
        """
        Bearish FVG:
        Candle 1 low > Candle 3 high
        """
        gaps = []

        for i in range(len(candles) - 2):
            c1 = candles[i]
            c3 = candles[i + 2]

            if c1["low"] > c3["high"]:
                gaps.append({
                    "type": "bearish",
                    "start": c3["high"],
                    "end": c1["low"],
                    "index": i
                })

        return gaps


if __name__ == "__main__":
    sample_data = [
        {"high": 100, "low": 95},
        {"high": 108, "low": 102},
        {"high": 115, "low": 110},
        {"high": 118, "low": 112},
    ]

    detector = FairValueGapDetector()

    print("Bullish FVGs:")
    print(detector.detect_bullish_fvg(sample_data))

    print("Bearish FVGs:")
    print(detector.detect_bearish_fvg(sample_data))
