class MarketStructureDetector:
    def __init__(self):
        pass

    def detect_bos(self, highs, lows):
        """
        Detect Break of Structure (BOS).
        """
        if len(highs) < 2 or len(lows) < 2:
            return None

        if highs[-1] > highs[-2]:
            return {
                "type": "bullish_bos",
                "level": highs[-2]
            }

        if lows[-1] < lows[-2]:
            return {
                "type": "bearish_bos",
                "level": lows[-2]
            }

        return None

    def detect_choch(self, trend, highs, lows):
        """
        Detect Change of Character (CHoCH).
        """
        if len(highs) < 2 or len(lows) < 2:
            return None

        if trend == "bullish" and lows[-1] < lows[-2]:
            return {
                "type": "bearish_choch",
                "level": lows[-2]
            }

        if trend == "bearish" and highs[-1] > highs[-2]:
            return {
                "type": "bullish_choch",
                "level": highs[-2]
            }

        return None


if __name__ == "__main__":
    highs = [3300, 3312, 3320]
    lows = [3288, 3295, 3305]

    detector = MarketStructureDetector()

    print(detector.detect_bos(highs, lows))
    print(detector.detect_choch("bullish", highs, lows))
