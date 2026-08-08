from smc_engine import SMCEngine
from entry_engine import EntryEngine


class SignalPipeline:
    """
    Connects M5 SMC output to the existing Entry Engine.

    CME intelligence/master signal is supplied externally.
    This layer converts M5 SMC structures into the exact
    confirmation format required by EntryEngine.
    """

    def __init__(self):
        self.smc = SMCEngine()
        self.entry = EntryEngine()

    @staticmethod
    def _fvg_bias(smc):
        fvg = smc.get("fvg")

        if not fvg:
            return "NONE"

        fvg_type = str(fvg.get("type", "")).lower()

        if fvg_type == "bullish_fvg":
            return "BULLISH"

        if fvg_type == "bearish_fvg":
            return "BEARISH"

        return "NONE"

    @staticmethod
    def _order_block_bias(smc):
        if smc.get("bullish_order_block"):
            return "BULLISH"

        if smc.get("bearish_order_block"):
            return "BEARISH"

        return "NONE"

    def evaluate(
        self,
        candles,
        master_signal,
        cme_levels,
        trend="bullish",
    ):
        smc = self.smc.analyze(
            candles,
            trend=trend,
        )

        fvg_bias = self._fvg_bias(smc)
        order_block_bias = self._order_block_bias(smc)

        entry = self.entry.evaluate(
            price=smc["price"],
            master_signal=master_signal,
            cme_levels=cme_levels,
            fvg_bias=fvg_bias,
            order_block_bias=order_block_bias,
        )

        return {
            "smc": smc,
            "fvg_bias": fvg_bias,
            "order_block_bias": order_block_bias,
            "entry": entry,
        }


if __name__ == "__main__":
    candles = [
        {"open": 3300, "high": 3310, "low": 3295, "close": 3298},
        {"open": 3298, "high": 3320, "low": 3296, "close": 3318},
        {"open": 3318, "high": 3330, "low": 3315, "close": 3328},
        {"open": 3328, "high": 3370, "low": 3325, "close": 3370},
    ]

    master_signal = {
        "valid": True,
        "signal": "BUY",
        "score": 7,
    }

    cme_levels = {
        "1sigma_upper": 3350,
        "1sigma_lower": 3310,
        "2sigma_upper": 3370,
        "2sigma_lower": 3290,
        "3sigma_upper": 3390,
        "3sigma_lower": 3270,
    }

    pipeline = SignalPipeline()

    print("=== SIGNAL PIPELINE TEST ===")
    result = pipeline.evaluate(
        candles=candles,
        master_signal=master_signal,
        cme_levels=cme_levels,
        trend="bullish",
    )

    print(result)
