from datetime import datetime, date


class CMEOptionsData:
    """
    CME options intelligence for a specifically selected
    CME expiration.

    Trading date and CME expiration date are deliberately
    kept separate.
    """

    def __init__(
        self,
        trading_date,
        expiration_date,
        data_timestamp=None,
        implied_volatility=None,
        gamma_exposure=None,
        open_interest=None,
        call_volume=None,
        put_volume=None,
        call_put_heatmap=None,
    ):
        self.trading_date = self._normalize_date(trading_date)
        self.expiration_date = self._normalize_date(expiration_date)
        self.data_timestamp = data_timestamp

        self.implied_volatility = implied_volatility
        self.gamma_exposure = gamma_exposure
        self.open_interest = open_interest

        self.call_volume = call_volume
        self.put_volume = put_volume
        self.call_put_heatmap = call_put_heatmap

    def validate(self):
        """
        Validate the relationship between trading date
        and the explicitly selected CME expiration.

        We DO NOT use DTE to select the contract.
        """

        if self.trading_date is None:
            return self._error("INVALID_TRADING_DATE")

        if self.expiration_date is None:
            return self._error("INVALID_EXPIRATION_DATE")

        # A contract from before the trading date is invalid.
        if self.expiration_date < self.trading_date:
            return self._error(
                "EXPIRATION_BEFORE_TRADING_DATE"
            )

        return {
            "valid": True,
            "reason": "DATES_VALIDATED",
            "trading_date": self.trading_date.isoformat(),
            "expiration_date": self.expiration_date.isoformat(),
        }

    def analyze(self):

        validation = self.validate()

        if not validation["valid"]:
            return {
                "available": False,
                "validation": validation,
            }

        return {
            "available": True,

            "trading_date":
                self.trading_date.isoformat(),

            "expiration_date":
                self.expiration_date.isoformat(),

            "data_timestamp":
                self.data_timestamp,

            "implied_volatility":
                self.implied_volatility,

            "gamma_exposure":
                self.gamma_exposure,

            "open_interest":
                self.open_interest,

            "call_volume":
                self.call_volume,

            "put_volume":
                self.put_volume,

            "call_put_heatmap":
                self.call_put_heatmap,

            "gamma_bias":
                self._gamma_bias(),

            "options_bias":
                self._options_bias(),

            "confidence":
                self._confidence(),
        }

    def _gamma_bias(self):

        if self.gamma_exposure is None:
            return "UNKNOWN"

        if self.gamma_exposure > 0:
            return "POSITIVE_GAMMA"

        if self.gamma_exposure < 0:
            return "NEGATIVE_GAMMA"

        return "NEUTRAL_GAMMA"

    def _options_bias(self):

        if (
            self.call_volume is None
            or self.put_volume is None
        ):
            return "UNKNOWN"

        if self.call_volume > self.put_volume:
            return "CALL_DOMINANT"

        if self.put_volume > self.call_volume:
            return "PUT_DOMINANT"

        return "BALANCED"

    def _confidence(self):

        score = 0

        if self.implied_volatility is not None:
            score += 1

        if self.gamma_exposure is not None:
            score += 1

        if self.open_interest is not None:
            score += 1

        if self.call_volume is not None:
            score += 1

        if self.put_volume is not None:
            score += 1

        if self.call_put_heatmap is not None:
            score += 1

        return score

    @staticmethod
    def _normalize_date(value):

        if value is None:
            return None

        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        if isinstance(value, str):

            value = value.strip()

            for fmt in (
                "%Y-%m-%d",
                "%Y/%m/%d",
                "%d-%m-%Y",
                "%d/%m/%Y",
            ):
                try:
                    return datetime.strptime(
                        value,
                        fmt
                    ).date()
                except ValueError:
                    continue

        return None

    @staticmethod
    def _error(reason):

        return {
            "valid": False,
            "reason": reason,
        }


if __name__ == "__main__":

    print("=== CME OPTIONS DATE TEST ===")

    options = CMEOptionsData(
        trading_date="2026-08-10",

        # Explicitly selected CME expiration.
        expiration_date="2026-08-11",

        data_timestamp="2026-08-10T00:30:00",

        implied_volatility=18.0,
        gamma_exposure=1250000,
        open_interest=8500,

        call_volume=3100,
        put_volume=2050,

        call_put_heatmap={
            "3300": {
                "call": 500,
                "put": 250,
            },
            "3350": {
                "call": 750,
                "put": 300,
            },
            "3400": {
                "call": 900,
                "put": 450,
            },
        },
    )

    print(options.analyze())

    print()
    print("=== EXPIRED CONTRACT TEST ===")

    expired = CMEOptionsData(
        trading_date="2026-08-10",
        expiration_date="2026-08-09",
    )

    print(expired.analyze())

