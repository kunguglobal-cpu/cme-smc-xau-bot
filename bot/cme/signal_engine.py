from datetime import date


class CMESignalEngine:

    def __init__(self, expected_range=None, options_data=None):
        self.expected_range = expected_range or {}
        self.options_data = options_data or {}

    def _score_expected_range(self, price):
        er = self.expected_range

        if not er:
            return 0, "UNKNOWN"

        levels = er.get("levels", {})

        upper_1 = levels.get("1sigma_upper")
        lower_1 = levels.get("1sigma_lower")
        upper_2 = levels.get("2sigma_upper")
        lower_2 = levels.get("2sigma_lower")

        score = 0
        bias = "NEUTRAL"

        if upper_1 and price >= upper_1:
            score += 2
            bias = "BEARISH_REJECTION_ZONE"

        elif lower_1 and price <= lower_1:
            score += 2
            bias = "BULLISH_REJECTION_ZONE"

        elif upper_2 and price >= upper_2:
            score += 3
            bias = "EXTREME_UPPER"

        elif lower_2 and price <= lower_2:
            score += 3
            bias = "EXTREME_LOWER"

        else:
            bias = "INSIDE_RANGE"

        return score, bias

    def _score_options(self):
        options = self.options_data

        if not options.get("available"):
            return 0, "UNKNOWN"

        score = 0

        gamma_bias = options.get("gamma_bias", "UNKNOWN")
        options_bias = options.get("options_bias", "UNKNOWN")

        if gamma_bias == "POSITIVE_GAMMA":
            score += 2
        elif gamma_bias == "NEGATIVE_GAMMA":
            score -= 2

        if options_bias == "CALL_DOMINANT":
            score += 2
        elif options_bias == "PUT_DOMINANT":
            score -= 2

        if score >= 3:
            bias = "BULLISH"
        elif score <= -3:
            bias = "BEARISH"
        else:
            bias = "NEUTRAL"

        return score, bias

    def _heatmap_bias(self):
        heatmap = self.options_data.get("call_put_heatmap", {})

        if not heatmap:
            return "UNKNOWN"

        calls = 0
        puts = 0

        for strike_data in heatmap.values():
            calls += strike_data.get("call", 0)
            puts += strike_data.get("put", 0)

        if calls > puts:
            return "CALL_DOMINANT"

        if puts > calls:
            return "PUT_DOMINANT"

        return "BALANCED"

    def analyze(self, price):
        er_score, er_bias = self._score_expected_range(price)
        option_score, option_bias = self._score_options()

        heatmap_bias = self._heatmap_bias()

        total_score = er_score + option_score

        if total_score >= 4:
            directional_bias = "BULLISH"

        elif total_score <= -4:
            directional_bias = "BEARISH"

        else:
            directional_bias = "NEUTRAL"

        return {
            "price": price,

            "expected_range_bias": er_bias,
            "expected_range_score": er_score,

            "gamma_bias": self.options_data.get(
                "gamma_bias",
                "UNKNOWN"
            ),

            "options_bias": option_bias,

            "heatmap_bias": heatmap_bias,

            "implied_volatility": self.options_data.get(
                "implied_volatility"
            ),

            "gamma_exposure": self.options_data.get(
                "gamma_exposure"
            ),

            "open_interest": self.options_data.get(
                "open_interest"
            ),

            "call_volume": self.options_data.get(
                "call_volume"
            ),

            "put_volume": self.options_data.get(
                "put_volume"
            ),

            "confluence_score": total_score,

            "directional_bias": directional_bias
        }


if __name__ == "__main__":

    expected_range = {
        "spot": 3330,
        "atm": 3330,
        "levels": {
            "1sigma_upper": 3350,
            "1sigma_lower": 3310,
            "2sigma_upper": 3370,
            "2sigma_lower": 3290,
            "3sigma_upper": 3390,
            "3sigma_lower": 3270
        }
    }

    options_data = {
        "available": True,
        "trading_date": "2026-08-10",
        "expiration_date": "2026-08-11",

        "implied_volatility": 18.0,
        "gamma_exposure": 1250000,
        "open_interest": 8500,

        "call_volume": 3100,
        "put_volume": 2050,

        "call_put_heatmap": {
            "3300": {
                "call": 500,
                "put": 250
            },
            "3350": {
                "call": 750,
                "put": 300
            },
            "3400": {
                "call": 900,
                "put": 450
            }
        },

        "gamma_bias": "POSITIVE_GAMMA",
        "options_bias": "CALL_DOMINANT"
    }

    engine = CMESignalEngine(
        expected_range,
        options_data
    )

    print("=== CME UNIFIED SIGNAL TEST ===")

    for price in [3290, 3310, 3330, 3350, 3370]:
        print()
        print(
            engine.analyze(price)
        )
