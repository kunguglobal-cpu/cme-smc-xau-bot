import pandas as pd

def detect_equal_highs(df, lookback=20, tolerance=0.20):
    """
    Finds equal highs (buy-side liquidity).
    """
    levels = []

    for i in range(lookback, len(df)):
        high = df.iloc[i]["high"]

        for j in range(i - lookback, i):
            if abs(high - df.iloc[j]["high"]) <= tolerance:
                levels.append({
                    "index": i,
                    "price": high,
                    "type": "BUY_LIQUIDITY"
                })

    return levels


def detect_equal_lows(df, lookback=20, tolerance=0.20):
    """
    Finds equal lows (sell-side liquidity).
    """
    levels = []

    for i in range(lookback, len(df)):
        low = df.iloc[i]["low"]

        for j in range(i - lookback, i):
            if abs(low - df.iloc[j]["low"]) <= tolerance:
                levels.append({
                    "index": i,
                    "price": low,
                    "type": "SELL_LIQUIDITY"
                })

    return levels
