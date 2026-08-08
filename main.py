from bot.signal_engine import SignalEngine
from bot.risk_manager import RiskManager
from bot.session_filter import SessionFilter


def get_market_data():
    """Temporary market data for testing."""
    opens = [3300, 3310, 3320]
    highs = [3315, 3325, 3338]
    lows = [3295, 3305, 3318]
    closes = [3310, 3322, 3335]

    return opens, highs, lows, closes


def main():
    account_balance = 10000
    risk_manager = RiskManager(account_balance, risk_percent=1)
    signal_engine = SignalEngine()
    session_filter = SessionFilter()

    if not session_filter.is_trading_session():
        print("Trading session closed.")
        return

    opens, highs, lows, closes = get_market_data()

    signal = signal_engine.generate_signal(
        opens,
        highs,
        lows,
        closes
    )

    print("Signal:", signal)

    if signal.get("direction") is None:
        print("No valid trade.")
        return

    stop_loss_points = 250
    value_per_point = 1.0

    lot_size = risk_manager.calculate_lot_size(
        stop_loss_points,
        value_per_point
    )

    print(f"Direction : {signal['direction']}")
    print(f"Lot Size  : {lot_size}")
    print("Ready to execute trade.")


if __name__ == "__main__":
    main()
