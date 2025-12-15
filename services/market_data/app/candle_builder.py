# candle_builder.py
import time
from collections import defaultdict

class CandleBuilder:
    def __init__(self, interval=60):
        self.interval = interval
        self.current = None

    def _bucket(self, ts):
        return ts - (ts % self.interval)

    def process_trade(self, price, qty, ts):
        bucket = self._bucket(ts)

        if not self.current or self.current["ts"] != bucket:
            self.current = {
                "ts": bucket,
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "volume": qty
            }
            return self.current, True

        self.current["high"] = max(self.current["high"], price)
        self.current["low"] = min(self.current["low"], price)
        self.current["close"] = price
        self.current["volume"] += qty

        return self.current, False
