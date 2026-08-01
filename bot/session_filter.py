from datetime import datetime, time
import pytz


class SessionFilter:
    def __init__(self):
        self.utc = pytz.UTC

    def is_trading_session(self):
        now = datetime.now(self.utc).time()

        # London Session (07:00–16:00 UTC)
        london_open = time(7, 0)
        london_close = time(16, 0)

        # New York Overlap (12:00–16:00 UTC)
        overlap_open = time(12, 0)
        overlap_close = time(16, 0)

        return (
            london_open <= now <= london_close or
            overlap_open <= now <= overlap_close
        )
