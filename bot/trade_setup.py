class TradeSetup:

    def _rr(self, direction, entry, stop_loss, take_profit):
        if direction == "BUY":
            risk = entry - stop_loss
            reward = take_profit - entry
        else:
            risk = stop_loss - entry
            reward = entry - take_profit

        if risk <= 0 or reward <= 0:
            return None

        return round(reward / risk, 2)

    def calculate(
        self,
        signal,
        price,
        cme_level=None,
        bullish_fvg=None,
        bearish_fvg=None,
        bullish_ob=None,
        bearish_ob=None,
        swing_high=None,
        swing_low=None,
        min_rr=2.0
    ):
        direction = signal.get("direction")

        if direction not in ("BUY", "SELL"):
            return {
                "valid": False,
                "reason": "No valid trading direction"
            }

        if cme_level is None:
            return {
                "valid": False,
                "reason": "CME expected-range level required"
            }

        entry = float(cme_level)
        price = float(price)

        if direction == "BUY":

            # Prefer bullish OB low, then bullish FVG bottom,
            # then swing low as protection.
            candidates = []

            if bullish_ob:
                candidates.append(float(bullish_ob["low"]))

            if bullish_fvg:
                candidates.append(float(bullish_fvg["bottom"]))

            if swing_low is not None:
                candidates.append(float(swing_low))

            candidates = [x for x in candidates if x < entry]

            if not candidates:
                return {
                    "valid": False,
                    "reason": "No valid bullish structure below entry"
                }

            stop_loss = min(candidates)

            # TP candidates: bearish OB high, bearish FVG top,
            # then swing high.
            targets = []

            if bearish_ob:
                targets.append(float(bearish_ob["high"]))

            if bearish_fvg:
                targets.append(float(bearish_fvg["top"]))

            if swing_high is not None:
                targets.append(float(swing_high))

            targets = [x for x in targets if x > entry]

            if not targets:
                return {
                    "valid": False,
                    "reason": "No valid bullish target above entry"
                }

            take_profit = min(targets)

        else:

            # Prefer bearish OB high, then bearish FVG top,
            # then swing high as protection.
            candidates = []

            if bearish_ob:
                candidates.append(float(bearish_ob["high"]))

            if bearish_fvg:
                candidates.append(float(bearish_fvg["top"]))

            if swing_high is not None:
                candidates.append(float(swing_high))

            candidates = [x for x in candidates if x > entry]

            if not candidates:
                return {
                    "valid": False,
                    "reason": "No valid bearish structure above entry"
                }

            stop_loss = max(candidates)

            # TP candidates: bullish OB low, bullish FVG bottom,
            # then swing low.
            targets = []

            if bullish_ob:
                targets.append(float(bullish_ob["low"]))

            if bullish_fvg:
                targets.append(float(bullish_fvg["bottom"]))

            if swing_low is not None:
                targets.append(float(swing_low))

            targets = [x for x in targets if x < entry]

            if not targets:
                return {
                    "valid": False,
                    "reason": "No valid bearish target below entry"
                }

            take_profit = max(targets)

        risk_reward = self._rr(
            direction,
            entry,
            stop_loss,
            take_profit
        )

        if risk_reward is None:
            return {
                "valid": False,
                "reason": "Invalid risk/reward geometry"
            }

        if risk_reward < min_rr:
            return {
                "valid": False,
                "reason": f"Risk/reward {risk_reward} below minimum {min_rr}",
                "direction": direction,
                "entry": entry,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "risk_reward": risk_reward
            }

        return {
            "valid": True,
            "direction": direction,
            "entry": entry,
            "price": price,
            "cme_level": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": risk_reward
        }


if __name__ == "__main__":

    setup = TradeSetup()

    bullish_signal = {
        "direction": "BUY",
        "reason": [
            "bullish_bos",
            "bullish_fvg",
            "bullish_order_block"
        ]
    }

    bullish_result = setup.calculate(
        signal=bullish_signal,
        price=3335,
        cme_level=3330,
        bullish_fvg={
            "type": "bullish_fvg",
            "top": 3315,
            "bottom": 3310
        },
        bullish_ob={
            "type": "bullish_order_block",
            "high": 3325,
            "low": 3305
        },
        swing_high=3340,
        swing_low=3295
    )

    print("=== BUY TEST ===")
    print(bullish_result)

    bearish_signal = {
        "direction": "SELL",
        "reason": [
            "bearish_bos",
            "bearish_fvg",
            "bearish_order_block"
        ]
    }

    bearish_result = setup.calculate(
        signal=bearish_signal,
        price=3325,
        cme_level=3330,
        bearish_fvg={
            "type": "bearish_fvg",
            "top": 3350,
            "bottom": 3340
        },
        bearish_ob={
            "type": "bearish_order_block",
            "high": 3355,
            "low": 3345
        },
        swing_high=3360,
        swing_low=3300
    )

    print("=== SELL TEST ===")
    print(bearish_result)
