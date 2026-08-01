class FairValueGapDetector:
    def __init__(self):
        pass

    def detect_fvg(self, highs, lows):
        """
        Detect Bullish and Bearish Fair Value Gaps.
        Requires at least 3 candles.
        """

        if len(highs) < 3 or len(lows) < 3:
            return None

        # Bullish FVG
        if lows[-1] > highs[-3]:
            return {
                "type": "bullish_fvg",
                "top": lows[-1],
                "bottom": highs[-3]
            }

        # Bearish FVG
        if highs[-1] < lows[-3]:
            return {
                "type": "bearish_fvg",
                "top": lows[-3],
                "bottom": highs[-1]
            }

        return None

    def is_mitigated(self, fvg, price):
        """
        Check whether price has mitigated the Fair Value Gap.
        """

        if fvg is None:
            return False

        if fvg["bottom"] <= price <= fvg["top"]:
            return True

        return False


if __name__ == "__main__":
    highs = [3300, 3312, 3320]
    lows = [3288, 3298, 3315]

    detector = FairValueGapDetector()

    fvg = detector.detect_fvg(highs, lows)
    print(fvg)

    if fvg:
        print(detector.is_mitigated(fvg, 3317))
