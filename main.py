from bot.signal_engine import SignalEngine
from bot.risk_manager import RiskManager
from bot.session_filter import SessionFilter


def get_market_data():
    """
    Placeholder for market data.
    This will later be replaced with live MT5 data.
    """
    opens = [3300, 3310, 3320]
    highs = [3315, 3325, 3338]
    lows = [3295, 3305, 3318]
    closes = [3310, 3322, 3335]

    return opens, highs, lows, closes


def main():

    signal_engine = SignalEngine()
    risk_manager = RiskManager(risk_percent=1)
    session_filter = SessionFilter()

    if not session_filter.is_trading_session():
        print("Trading session closed.")
        return

    opens, highs, lows, closes = get_market_data()

    signal = signal_engine.generate_signal(opens, highs, lows, closes)

    print("Signal:", signal)

    if signal["direction"] is None:
        print("No valid trade.")
        return

    account_balance = 10000
    stop_loss_points = 250

    lot_size = risk_manager.calculate_lot_size(
        account_balance,
        stop_loss_points
    )

    print(f"Direction : {signal['direction']}")
    print(f"Lot Size  : {lot_size}")

    # MT5 order execution will be added here
    print("Ready to execute trade.")


if __name__ == "__main__":
    main()
