from datetime import date, datetime


class CMEEngine:
    """
    CME intelligence engine.

    Important:
    CME option data is selected by the exact target expiration/trading
    date, NOT by the smallest DTE.
    """

    def __init__(self, expected_range=None):
        self.expected_range = expected_range

    def select_expiration(self, expirations, target_date):
        """
        Select the CME expiration matching the exact target date.

        expirations can contain:
            {
                "expiration_date": "2026-08-10",
                "dte": 0.85,
                ...
            }
        """

        target = self._normalize_date(target_date)

        if target is None:
            return {
                "available": False,
                "reason": "INVALID_TARGET_DATE",
                "expiration": None,
            }

        valid = []

        for contract in expirations or []:
            expiration = self._normalize_date(
                contract.get("expiration_date")
            )

            if expiration is None:
                continue

            # Never accept an already-expired contract.
            if expiration < target:
                continue

            # Exact-date matching only.
            if expiration == target:
                valid.append(contract)

        if not valid:
            return {
                "available": False,
                "reason": "CME_DATA_UNAVAILABLE_FOR_TARGET_DATE",
                "target_date": target.isoformat(),
                "expiration": None,
            }

        # If multiple records exist for the same expiration,
        # choose the one with the latest data timestamp.
        valid.sort(
            key=lambda x: self._timestamp_value(
                x.get("data_timestamp")
            ),
            reverse=True,
        )

        selected = valid[0]

        return {
            "available": True,
            "reason": "EXACT_EXPIRATION_MATCH",
            "target_date": target.isoformat(),
            "expiration": selected,
        }

    def build_market_map(
        self,
        price,
        target_date,
        expirations=None,
    ):
        """
        Build the CME market map for one specific trading date.
        """

        selection = self.select_expiration(
            expirations or [],
            target_date,
        )

        result = {
            "available": False,
            "trading_date": self._normalize_date(
                target_date
            ).isoformat()
            if self._normalize_date(target_date)
            else None,
            "expiration": None,
            "expected_range": None,
            "options": None,
            "directional_bias": "NEUTRAL",
            "confluence_score": 0,
        }

        if not selection["available"]:
            result["reason"] = selection["reason"]
            return result

        contract = selection["expiration"]

        result["available"] = True
        result["expiration"] = contract

        if self.expected_range is not None:
            result["expected_range"] = self.expected_range.to_dict(
                price
            )

        # These fields will be populated by the CME options
        # data adapter as we build the next modules.
        result["options"] = {
            "available": False,
            "implied_volatility": contract.get(
                "implied_volatility"
            ),
            "gamma_exposure": contract.get(
                "gamma_exposure"
            ),
            "open_interest": contract.get(
                "open_interest"
            ),
            "call_put_heatmap": contract.get(
                "call_put_heatmap"
            ),
        }

        return result

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
    def _timestamp_value(value):
        if not value:
            return 0

        if isinstance(value, (int, float)):
            return value

        try:
            return datetime.fromisoformat(
                str(value).replace("Z", "+00:00")
            ).timestamp()
        except ValueError:
            return 0


if __name__ == "__main__":

    print("=== CME DATE-AWARE ENGINE TEST ===")

    engine = CMEEngine()

    expirations = [
        {
            "expiration_date": "2026-08-07",
            "dte": 0.1,
            "data_timestamp": "2026-08-07T14:00:00",
        },
        {
            "expiration_date": "2026-08-10",
            "dte": 2.7,
            "data_timestamp": "2026-08-08T00:30:00",
        },
        {
            "expiration_date": "2026-08-11",
            "dte": 3.7,
            "data_timestamp": "2026-08-08T00:30:00",
        },
    ]

    print(
        engine.select_expiration(
            expirations,
            "2026-08-10",
        )
    )

    print("\n=== WRONG DATE TEST ===")

    print(
        engine.select_expiration(
            expirations,
            "2026-08-09",
        )
    )

