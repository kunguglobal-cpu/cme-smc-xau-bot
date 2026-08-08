from market_structure import MarketStructureDetector
from fvg_detector import FairValueGapDetector
from order_block_detector import OrderBlockDetector
from liquidity_sweep import LiquiditySweepDetector
from m5_data_adapter import M5DataAdapter


class SMCEngine:
    """
    Runs the existing M5 SMC detectors against one normalized
    M5 candle dataset.
    """

    def __init__(self):
        self.adapter = M5DataAdapter()
        self.market_structure = MarketStructureDetector()
        self.fvg = FairValueGapDetector()
        self.order_block = OrderBlockDetector()
        self.liquidity = LiquiditySweepDetector()

    def analyze(self, candles, trend="bullish"):
        data = self.adapter.snapshot(candles)

        opens = data["opens"]
        highs = data["highs"]
        lows = data["lows"]
        closes = data["closes"]

        bos = self.market_structure.detect_bos(
            highs,
            lows
        )

        choch = self.market_structure.detect_choch(
            trend,
            highs,
            lows
        )

        fvg = self.fvg.detect_fvg(
            highs,
            lows
        )

        bullish_ob = self.order_block.detect_bullish_ob(
            opens,
            highs,
            lows,
            closes
        )

        bearish_ob = self.order_block.detect_bearish_ob(
            opens,
            highs,
            lows,
            closes
        )

        buy_side_sweep = self.liquidity.detect_buy_side_sweep(
            highs,
            closes
        )

        sell_side_sweep = self.liquidity.detect_sell_side_sweep(
            lows,
            closes
        )

        return {
            "timeframe": "M5",
            "bars": data["bars"],
            "price": data["last_close"],
            "bos": bos,
            "choch": choch,
            "fvg": fvg,
            "bullish_order_block": bullish_ob,
            "bearish_order_block": bearish_ob,
            "buy_side_sweep": buy_side_sweep,
            "sell_side_sweep": sell_side_sweep,
        }


if __name__ == "__main__":
    sample = [
        {"open": 3300, "high": 3310, "low": 3295, "close": 3298},
        {"open": 3298, "high": 3320, "low": 3296, "close": 3318},
        {"open": 3318, "high": 3330, "low": 3315, "close": 3328},
        {"open": 3328, "high": 3340, "low": 3325, "close": 3338},
    ]

    engine = SMCEngine()

    print("=== M5 SMC ENGINE TEST ===")
    print(engine.analyze(sample))
