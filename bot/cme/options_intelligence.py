class OptionsIntelligence:

    def __init__(self, data=None):
        self.data = data or {}

    def analyze(self):
        # Accept either raw CME data or the analyzed CMEOptionsData result.
        iv = self.data.get("implied_volatility")
        gex = self.data.get("gamma_exposure")
        oi = self.data.get("open_interest")
        heatmap = self.data.get("call_put_heatmap")

        call_volume = self.data.get("call_volume")
        put_volume = self.data.get("put_volume")

        gamma_bias = self.data.get("gamma_bias")
        options_bias = self.data.get("options_bias")
        confidence = self.data.get("confidence")

        # If CMEOptionsData already analyzed the data,
        # preserve that intelligence.
        if gamma_bias is not None or options_bias is not None:
            return {
                "available": bool(self.data.get("available", False)),
                "implied_volatility": iv,
                "gamma_exposure": gex,
                "open_interest": oi,
                "call_volume": call_volume,
                "put_volume": put_volume,
                "call_put_heatmap": heatmap,
                "gamma_bias": gamma_bias or "UNKNOWN",
                "options_bias": options_bias or "UNKNOWN",
                "confidence": confidence if confidence is not None else 0,
            }

        # Raw-data fallback.
        result = {
            "available": False,
            "implied_volatility": iv,
            "gamma_exposure": gex,
            "open_interest": oi,
            "call_volume": call_volume,
            "put_volume": put_volume,
            "call_put_heatmap": heatmap,
            "gamma_bias": "UNKNOWN",
            "options_bias": "UNKNOWN",
            "confidence": 0,
        }

        if not any([
            iv,
            gex,
            oi,
            call_volume,
            put_volume,
            heatmap
        ]):
            return result

        result["available"] = True
        return result


if __name__ == "__main__":
    engine = OptionsIntelligence()

    print("=== CME OPTIONS INTELLIGENCE TEST ===")
    print(engine.analyze())
