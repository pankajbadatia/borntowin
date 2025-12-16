# main.py
import asyncio
from fastapi import FastAPI
from app.binance_ws import BinanceWS
from app.redis_store import get_json 
from app.settings import SYMBOL, STALE_THRESHOLD

app = FastAPI()
ws = BinanceWS(SYMBOL)

@app.get("/health")
def health():
    return get_json("market:data_status")

@app.on_event("startup")
async def startup():
    asyncio.create_task(ws.run_forever())


