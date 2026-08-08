from bot.logger import log_signal
from bot.market_structure import MarketStructureDetector
from bot.fvg_detector import FairValueGapDetector
from bot.order_block_detector import OrderBlockDetector
from bot.liquidity_sweep import LiquiditySweepDetector


class SignalEngine:

    def __init__(self):
        self.market = MarketStructureDetector()
        self.fvg = FairValueGapDetector()
        self.ob = OrderBlockDetector()
        self.liquidity = LiquiditySweepDetector()

    def generate_signal(self, o, h, l, c):

        signal = {
            "direction": None,
            "reason": []
        }

        bos = self.market.detect_bos(h, l)

        if bos:
            signal["reason"].append(bos["type"])

        fvg = self.fvg.detect_fvg(h, l)

        if fvg:
            signal["reason"].append(fvg["type"])

        bull_ob = self.ob.detect_bullish_ob(o, h, l, c)

        if bull_ob:
            signal["reason"].append("bullish_order_block")

        bear_ob = self.ob.detect_bearish_ob(o, h, l, c)

        if bear_ob:
            signal["reason"].append("bearish_order_block")

        buy_sweep = self.liquidity.detect_buy_side_sweep(h, c)

        if buy_sweep:
            signal["reason"].append("buy_side_sweep")

        sell_sweep = self.liquidity.detect_sell_side_sweep(l, c)

        if sell_sweep:
            signal["reason"].append("sell_side_sweep")

        # Buy setup
        if (
            "bullish_bos" in signal["reason"]
            and ("bullish_order_block" in signal["reason"] or "bullish_fvg" in signal["reason"])
        ):
            signal["direction"] = "BUY"

        # Sell setup
        if (
            "bearish_bos" in signal["reason"]
            and ("bearish_order_block" in signal["reason"] or "bearish_fvg" in signal["reason"])
        ):
            signal["direction"] = "SELL"

        log_signal(signal)
        return signal


if __name__ == "__main__":

    opens = [3300, 3310, 3320]
    highs = [3315, 3325, 3338]
    lows = [3295, 3305, 3318]
    closes = [3310, 3322, 3335]

    engine = SignalEngine()

    print(engine.generate_signal(opens, highs, lows, closes))
