# binance_ws.py
import json
import time
import websockets
import asyncio
from app.candle_builder import CandleBuilder
from app.redis_store import set_json, update_data_status

WS_URL = "wss://stream.binance.com:9443/ws"

class BinanceWS:
    def __init__(self, symbol):
        self.symbol = symbol.lower()
        self.candle_builder = CandleBuilder()

    async def connect(self):
        stream = f"{self.symbol}@trade"
        async with websockets.connect(f"{WS_URL}/{stream}") as ws:
            update_data_status(connected=True)
            async for msg in ws:
                data = json.loads(msg)
                self.handle_trade(data)

    def handle_trade(self, data):
        price = float(data["p"])
        qty = float(data["q"])
        ts = data["T"] // 1000

        candle, new_candle = self.candle_builder.process_trade(price, qty, ts)

        set_json("market:last_trade", data)
        set_json("market:candles:1m", candle)

        update_data_status(
            last_trade_ts=ts,
            stale=False
        )

    async def run_forever(self):
        while True:
            try:
                await self.connect()
            except Exception as e:
                update_data_status(connected=False)
                await asyncio.sleep(2)
