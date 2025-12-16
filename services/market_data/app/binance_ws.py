import json
import asyncio
import websockets
from app.candle_builder import CandleBuilder
from app.redis_store import set_json, update_data_status, lpush_json

WS_URL = "wss://stream.binance.com:9443/stream"


class BinanceWS:
    def __init__(self, symbol: str):
        self.symbol = symbol.lower()
        self.candle_builder = CandleBuilder()

    async def connect(self):
        """
        Connect to Binance combined streams:
        - trade (for candles)
        - bookTicker (for bid/ask spread)
        """
        streams = f"{self.symbol}@trade/{self.symbol}@bookTicker"
        url = f"{WS_URL}?streams={streams}"

        async with websockets.connect(url) as ws:
            update_data_status(connected=True)

            async for msg in ws:
                payload = json.loads(msg)

                stream = payload.get("stream", "")
                data = payload.get("data", {})

                # Route by stream name (MOST RELIABLE)
                if stream.endswith("@trade"):
                    self.handle_trade(data)

                elif stream.endswith("@bookTicker"):
                    self.handle_book_ticker(data)

    def handle_trade(self, data: dict):
        """
        Handle trade events:
        - update candles
        - persist closed candles
        - update data health
        """
        price = float(data["p"])
        qty = float(data["q"])
        ts = data["T"] // 1000

        closed, current, is_closed = self.candle_builder.process_trade(price, qty, ts)

        # Latest in-progress candle (always update)
        set_json("market:candles:1m", current)

        # Persist closed candles
        if is_closed and closed:
            lpush_json("market:candles:1m:list", closed, max_len=500)

            # ✅ IMPORTANT: candle close counts as fresh data
            update_data_status(
                connected=True,
                last_trade_ts=closed["ts"],

            )

        # Always record last trade (even if candle not closed)
        set_json("market:last_trade", data)


    def handle_book_ticker(self, data: dict):
        """
        Handle best bid / ask updates
        """
        best = {
            "bid": float(data["b"]),
            "ask": float(data["a"]),
            "ts": data["E"] // 1000,
        }
        set_json("market:best_bid_ask", best)

    async def run_forever(self):
        """
        Auto-reconnect loop
        """
        while True:
            try:
                await self.connect()
            except Exception:
                update_data_status(connected=False)
                await asyncio.sleep(2)
