class CandleBuilder:
    def __init__(self, interval=60):
        self.interval = interval
        self.current = None

    def _bucket(self, ts):
        return ts - (ts % self.interval)

    def process_trade(self, price, qty, ts):
        bucket = self._bucket(ts)

        # first candle
        if not self.current:
            self.current = {
                "ts": bucket, "open": price, "high": price, "low": price,
                "close": price, "volume": qty
            }
            return None, self.current, False  # closed=None

        # new candle starts -> previous becomes "closed"
        if bucket != self.current["ts"]:
            closed = self.current
            self.current = {
                "ts": bucket, "open": price, "high": price, "low": price,
                "close": price, "volume": qty
            }
            return closed, self.current, True

        # same candle
        self.current["high"] = max(self.current["high"], price)
        self.current["low"] = min(self.current["low"], price)
        self.current["close"] = price
        self.current["volume"] += qty
        return None, self.current, False
