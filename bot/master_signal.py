class MasterSignal:

    def __init__(
        self,
        cme=None,
        smc=None,
        price=None,
        session_allowed=True
    ):
        self.cme = cme or {}
        self.smc = smc or {}
        self.price = price
        self.session_allowed = session_allowed

    def calculate(self):

        score = 0
        reasons = []

        # =========================
        # CME DIRECTION
        # =========================

        cme_bias = self.cme.get(
            "directional_bias",
            "NEUTRAL"
        )

        if cme_bias == "BULLISH":
            score += 2
            reasons.append("cme_bullish")

        elif cme_bias == "BEARISH":
            score -= 2
            reasons.append("cme_bearish")

        # =========================
        # GAMMA
        # =========================

        gamma = self.cme.get(
            "gamma_bias",
            "UNKNOWN"
        )

        if gamma == "POSITIVE_GAMMA":
            score += 1
            reasons.append("positive_gamma")

        elif gamma == "NEGATIVE_GAMMA":
            score -= 1
            reasons.append("negative_gamma")

        # =========================
        # OPTIONS
        # =========================

        options = self.cme.get(
            "options_bias",
            "UNKNOWN"
        )

        if options == "CALL_DOMINANT":
            score += 1
            reasons.append("call_dominant")

        elif options == "PUT_DOMINANT":
            score -= 1
            reasons.append("put_dominant")

        # =========================
        # HEATMAP
        # =========================

        heatmap = self.cme.get(
            "heatmap_bias",
            "UNKNOWN"
        )

        if heatmap == "CALL_DOMINANT":
            score += 1
            reasons.append("call_heatmap")

        elif heatmap == "PUT_DOMINANT":
            score -= 1
            reasons.append("put_heatmap")

        # =========================
        # SMC
        # =========================

        smc_bias = self.smc.get(
            "direction",
            "NEUTRAL"
        )

        if smc_bias == "BULLISH":
            score += 2
            reasons.append("smc_bullish")

        elif smc_bias == "BEARISH":
            score -= 2
            reasons.append("smc_bearish")

        # =========================
        # FINAL DECISION
        # =========================

        if score >= 6:
            signal = "BUY"
            valid = True

        elif score <= -6:
            signal = "SELL"
            valid = True

        else:
            signal = "NO_TRADE"
            valid = False

        return {
            "valid": valid,
            "signal": signal,
            "score": score,
            "price": self.price,
            "cme_bias": cme_bias,
            "gamma_bias": gamma,
            "options_bias": options,
            "heatmap_bias": heatmap,
            "smc_bias": smc_bias,
            "reasons": reasons
        }


if __name__ == "__main__":

    print("=== MASTER SIGNAL ENGINE TEST ===")

    cme = {
        "directional_bias": "BULLISH",
        "gamma_bias": "POSITIVE_GAMMA",
        "options_bias": "CALL_DOMINANT",
        "heatmap_bias": "CALL_DOMINANT"
    }

    smc = {
        "direction": "BULLISH"
    }

    engine = MasterSignal(
        cme=cme,
        smc=smc,
        price=3330,
        session_allowed=True
    )

    print(engine.calculate())

    print()
    print("=== CONFLICT TEST ===")

    smc = {
        "direction": "BEARISH"
    }

    engine = MasterSignal(
        cme=cme,
        smc=smc,
        price=3350,
        session_allowed=True
    )

    print(engine.calculate())

    print()
    print("=== SESSION TEST ===")

    engine = MasterSignal(
        cme=cme,
        smc={"direction": "BULLISH"},
        price=3330,
        session_allowed=False
    )

    print(engine.calculate())
