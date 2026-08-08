"""
CME SMC XAU BOT - ENTRY ENGINE

Final entry confirmation layer.

Rules:
1. Master signal must be BUY or SELL.
2. Price must be at a CME expected-range level/zone.
3. M5 FVG or Order Block must confirm the direction.
4. All required confirmations must agree.
5. Otherwise: NO_TRADE.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class EntryEngine:
    tolerance: float = 2.0

    def _near_level(self, price: float, level: float) -> bool:
        return abs(float(price) - float(level)) <= self.tolerance

    def _price_at_cme_level(
        self,
        price: float,
        cme_levels: Dict[str, float]
    ) -> Optional[str]:

        for name, level in cme_levels.items():
            if self._near_level(price, level):
                return name

        return None

    def evaluate(
        self,
        price: float,
        master_signal: Dict[str, Any],
        cme_levels: Dict[str, float],
        fvg_bias: str = "NONE",
        order_block_bias: str = "NONE",
    ) -> Dict[str, Any]:

        signal = master_signal.get("signal", "NO_TRADE")

        result = {
            "valid": False,
            "entry": False,
            "signal": "NO_TRADE",
            "price": float(price),
            "cme_level": None,
            "confirmation": None,
            "reason": "NO_TRADE",
        }

        # Master signal must be valid
        if not master_signal.get("valid", False):
            result["reason"] = "MASTER_SIGNAL_INVALID"
            return result

        if signal not in ("BUY", "SELL"):
            result["reason"] = "NO_DIRECTIONAL_SIGNAL"
            return result

        # Price must be near a CME expected-range level
        cme_level = self._price_at_cme_level(price, cme_levels)

        if cme_level is None:
            result["reason"] = "PRICE_NOT_AT_CME_LEVEL"
            return result

        # Normalize confirmations
        fvg = str(fvg_bias).upper()
        ob = str(order_block_bias).upper()

        # BUY confirmation
        if signal == "BUY":

            if fvg == "BULLISH":
                confirmation = "FVG_BULLISH"
            elif ob == "BULLISH":
                confirmation = "ORDER_BLOCK_BULLISH"
            else:
                result["reason"] = "NO_BULLISH_SMC_CONFIRMATION"
                return result

            result.update({
                "valid": True,
                "entry": True,
                "signal": "BUY",
                "cme_level": cme_level,
                "confirmation": confirmation,
                "reason": "BUY_ENTRY_CONFIRMED",
            })

            return result

        # SELL confirmation
        if signal == "SELL":

            if fvg == "BEARISH":
                confirmation = "FVG_BEARISH"
            elif ob == "BEARISH":
                confirmation = "ORDER_BLOCK_BEARISH"
            else:
                result["reason"] = "NO_BEARISH_SMC_CONFIRMATION"
                return result

            result.update({
                "valid": True,
                "entry": True,
                "signal": "SELL",
                "cme_level": cme_level,
                "confirmation": confirmation,
                "reason": "SELL_ENTRY_CONFIRMED",
            })

            return result

        return result


if __name__ == "__main__":

    engine = EntryEngine()

    cme_levels = {
        "1sigma_upper": 3350,
        "1sigma_lower": 3310,
        "2sigma_upper": 3370,
        "2sigma_lower": 3290,
        "3sigma_upper": 3390,
        "3sigma_lower": 3270,
    }

    master_signal = {
        "valid": True,
        "signal": "BUY",
        "score": 7,
    }

    print("=== ENTRY ENGINE TEST ===")

    print(
        engine.evaluate(
            price=3310,
            master_signal=master_signal,
            cme_levels=cme_levels,
            fvg_bias="BULLISH",
            order_block_bias="NONE",
        )
    )

    print("\n=== NO CME LEVEL TEST ===")

    print(
        engine.evaluate(
            price=3330,
            master_signal=master_signal,
            cme_levels=cme_levels,
            fvg_bias="BULLISH",
            order_block_bias="NONE",
        )
    )

    print("\n=== NO SMC CONFIRMATION TEST ===")

    print(
        engine.evaluate(
            price=3310,
            master_signal=master_signal,
            cme_levels=cme_levels,
            fvg_bias="NONE",
            order_block_bias="NONE",
        )
    )
