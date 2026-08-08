class ExpectedRange:
    """
    CME Expected Range data handler.

    The module is deliberately independent from the CME connection.
    Later, real CME/QuikStrike data can be fed into this class without
    changing the trading logic.
    """

    def __init__(
        self,
        spot,
        atm=None,
        upper_1sigma=None,
        lower_1sigma=None,
        upper_2sigma=None,
        lower_2sigma=None,
        upper_3sigma=None,
        lower_3sigma=None,
    ):
        self.spot = float(spot)
        self.atm = float(atm) if atm is not None else self.spot

        self.levels = {
            "1sigma_upper": self._number(upper_1sigma),
            "1sigma_lower": self._number(lower_1sigma),
            "2sigma_upper": self._number(upper_2sigma),
            "2sigma_lower": self._number(lower_2sigma),
            "3sigma_upper": self._number(upper_3sigma),
            "3sigma_lower": self._number(lower_3sigma),
        }

    @staticmethod
    def _number(value):
        if value is None:
            return None
        return float(value)

    def available_levels(self):
        """Return only levels that contain data."""
        return {
            name: value
            for name, value in self.levels.items()
            if value is not None
        }

    def nearest_level(self, price=None):
        """Return the CME expected-range level closest to price."""
        if price is None:
            price = self.spot

        price = float(price)

        levels = self.available_levels()

        if not levels:
            return None

        name, value = min(
            levels.items(),
            key=lambda item: abs(item[1] - price)
        )

        return {
            "name": name,
            "price": value,
            "distance": abs(value - price),
        }

    def zone(self, price=None):
        """
        Identify where price is relative to the expected range.
        """
        if price is None:
            price = self.spot

        price = float(price)

        u1 = self.levels["1sigma_upper"]
        l1 = self.levels["1sigma_lower"]
        u2 = self.levels["2sigma_upper"]
        l2 = self.levels["2sigma_lower"]
        u3 = self.levels["3sigma_upper"]
        l3 = self.levels["3sigma_lower"]

        if u3 is not None and price >= u3:
            return "ABOVE_3SIGMA"

        if u2 is not None and price >= u2:
            return "2_TO_3SIGMA_UP"

        if u1 is not None and price >= u1:
            return "1_TO_2SIGMA_UP"

        if l1 is not None and price >= l1:
            if u1 is not None and price <= u1:
                return "INSIDE_1SIGMA"

        if l2 is not None and price >= l2:
            return "1_TO_2SIGMA_DOWN"

        if l3 is not None and price >= l3:
            return "2_TO_3SIGMA_DOWN"

        if l3 is not None and price < l3:
            return "BELOW_3SIGMA"

        return "UNDEFINED"

    def bias(self, price=None):
        """
        Basic expected-range location bias.

        This is NOT a trade signal.
        SMC confirmation will be required later.
        """
        zone = self.zone(price)

        if zone in (
            "ABOVE_3SIGMA",
            "2_TO_3SIGMA_UP",
        ):
            return "BEARISH_LOCATION"

        if zone in (
            "BELOW_3SIGMA",
            "2_TO_3SIGMA_DOWN",
        ):
            return "BULLISH_LOCATION"

        return "NEUTRAL_LOCATION"

    def to_dict(self, price=None):
        """Return a clean structure for the signal engine."""
        if price is None:
            price = self.spot

        nearest = self.nearest_level(price)

        return {
            "spot": self.spot,
            "atm": self.atm,
            "levels": self.levels,
            "zone": self.zone(price),
            "bias": self.bias(price),
            "nearest_level": nearest,
        }


if __name__ == "__main__":
    er = ExpectedRange(
        spot=3330,
        atm=3330,
        upper_1sigma=3350,
        lower_1sigma=3310,
        upper_2sigma=3370,
        lower_2sigma=3290,
        upper_3sigma=3390,
        lower_3sigma=3270,
    )

    print("=== CME EXPECTED RANGE TEST ===")
    print(er.to_dict())
