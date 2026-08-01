from datetime import datetime, time


class SessionFilter:
    """
    Filters trades to the London and New York overlap.
    Times are in UTC by default.
    Adjust if your broker server uses a different timezone.
    """

    def __init__(self):
        self.start = time(13, 0)   # 13:00 UTC
        self.end = time(16, 0)     # 16:00 UTC

    def is_trading_session(self, current_time=None):
        if current_time is None:
            current_time = datetime.utcnow().time()

        return self.start <= current_time <= self.end


if __name__ == "__main__":
    sf = SessionFilter()

    if sf.is_trading_session():
        print("Trading session is OPEN")
    else:
        print("Trading session is CLOSED")
