from datetime import datetime, timezone
import pandas as pd


class M5DataAdapter:
    """
    Normalizes XAUUSD M5 OHLC candle data for the SMC detectors.
    """

    REQUIRED_COLUMNS = ["open", "high", "low", "close"]

    def normalize(self, candles):
        """
        Accept a pandas DataFrame or list of candle dictionaries.

        Required fields:
            open, high, low, close

        Optional:
            time / timestamp
        """

        if isinstance(candles, pd.DataFrame):
            df = candles.copy()
        else:
            df = pd.DataFrame(candles)

        if df.empty:
            raise ValueError("No M5 candles supplied")

        # Normalize column names.
        df.columns = [str(c).lower() for c in df.columns]

        missing = [
            column for column in self.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required M5 columns: {missing}"
            )

        for column in self.REQUIRED_COLUMNS:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        df = df.dropna(
            subset=self.REQUIRED_COLUMNS
        ).reset_index(drop=True)

        if df.empty:
            raise ValueError("No valid M5 OHLC candles remain")

        return df

    def snapshot(self, candles, bars=100):
        """
        Return the latest M5 OHLC arrays required by the
        existing SMC detectors.
        """

        df = self.normalize(candles)

        df = df.tail(bars).reset_index(drop=True)

        return {
            "opens": df["open"].tolist(),
            "highs": df["high"].tolist(),
            "lows": df["low"].tolist(),
            "closes": df["close"].tolist(),
            "bars": len(df),
            "last_close": float(df["close"].iloc[-1]),
        }


if __name__ == "__main__":
    sample = [
        {
            "open": 3330,
            "high": 3335,
            "low": 3325,
            "close": 3332,
        },
        {
            "open": 3332,
            "high": 3340,
            "low": 3329,
            "close": 3338,
        },
        {
            "open": 3338,
            "high": 3348,
            "low": 3335,
            "close": 3345,
        },
    ]

    adapter = M5DataAdapter()
    result = adapter.snapshot(sample)

    print("=== M5 DATA ADAPTER TEST ===")
    print("bars:", result["bars"])
    print("opens:", result["opens"])
    print("highs:", result["highs"])
    print("lows:", result["lows"])
    print("closes:", result["closes"])
    print("last_close:", result["last_close"])
