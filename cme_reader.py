"""CME expected-range data adapter."""

from numbers import Real


class CMEReader:

    def __init__(self):
        self.snapshot = None
        self.expected_high = None
        self.expected_low = None

    @staticmethod
    def _number(value):
        if value is None or value == "":
            return None

        if isinstance(value, Real):
            return float(value)

        text = str(value).strip().replace(",", "")

        try:
            return float(text)
        except ValueError:
            return None

    @staticmethod
    def _first(data, *keys):
        for key in keys:
            if key in data and data[key] not in (None, ""):
                return data[key]
        return None

    def update_range(self, high, low):
        """Backward-compatible 1-sigma range update."""
        self.expected_high = self._number(high)
        self.expected_low = self._number(low)

    def read_snapshot(self, data):
        """Convert CME/QuikStrike data into our internal format.

        Supports either direct price levels or expected-move distances.
        """

        if not isinstance(data, dict):
            raise TypeError("CME snapshot must be a dictionary")

        spot = self._number(
            self._first(
                data,
                "futures_price",
                "futures",
                "spot",
                "atm"
            )
        )

        atm = self._number(
            self._first(data, "atm", "atm_price")
        )

        if atm is None:
            atm = spot

        if spot is None:
            raise ValueError(
                "CME snapshot requires futures_price, futures, spot or atm"
            )

        levels = {}

        for sigma in (1, 2, 3):

            upper = self._number(
                self._first(
                    data,
                    f"{sigma}sigma_upper",
                    f"upper_{sigma}sigma",
                    f"expected_high_{sigma}sd"
                )
            )

            lower = self._number(
                self._first(
                    data,
                    f"{sigma}sigma_lower",
                    f"lower_{sigma}sigma",
                    f"expected_low_{sigma}sd"
                )
            )

            move = self._number(
                self._first(
                    data,
                    f"expected_move_{sigma}sd",
                    f"range_{sigma}sd",
                    f"{sigma}sd",
                    f"expected_range_{sigma}sd"
                )
            )

            if move is not None:

                if upper is None:
                    upper = atm + move

                if lower is None:
                    lower = atm - move

            levels[f"{sigma}sigma_upper"] = upper
            levels[f"{sigma}sigma_lower"] = lower

        self.snapshot = {
            "symbol": self._first(
                data,
                "symbol",
                "product",
                "underlying"
            ),

            "expiry": self._first(
                data,
                "expiry",
                "expiration",
                "expiration_date"
            ),

            "futures_price": spot,

            "atm": atm,

            "volatility": self._number(
                self._first(
                    data,
                    "volatility",
                    "implied_volatility",
                    "iv"
                )
            ),

            "levels": levels
        }

        self.expected_high = levels["1sigma_upper"]
        self.expected_low = levels["1sigma_lower"]

        return self.get_snapshot()

    def get_snapshot(self):

        if self.snapshot is None:
            return None

        return {
            **self.snapshot,
            "levels": dict(self.snapshot["levels"])
        }

    def get_range(self):
        """Return the existing 1-sigma range interface."""
        return {
            "high": self.expected_high,
            "low": self.expected_low
        }


if __name__ == "__main__":

    reader = CMEReader()

    snapshot = reader.read_snapshot({

        "symbol": "OG",

        "expiry": "G1MQ6",

        "futures_price": 4076.6,

        "volatility": 14.14,

        "expected_move_1sd": 42.9,

        "expected_move_2sd": 86.5,

        "expected_move_3sd": 130.5
    })

    print("=== CME READER TEST ===")

    print(snapshot)

    print()

    print("=== 1-SIGMA RANGE ===")

    print(reader.get_range())
