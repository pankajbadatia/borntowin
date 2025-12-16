import asyncio, time
from fastapi import FastAPI
from app.redis_store import get_json, set_json, lrange_json
from app.settings import (
    CANDLE_LIST_KEY, LATEST_CANDLE_KEY, BEST_BID_ASK_KEY,
    FEATURE_KEY, CALIB_KEY, WINDOW
)
from app.compute import compute_features

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True, "ts": int(time.time())}

@app.get("/features")
def features():
    return get_json(FEATURE_KEY) or {}

@app.on_event("startup")
async def startup():
    asyncio.create_task(loop())

async def loop():
    while True:
        candles = lrange_json(CANDLE_LIST_KEY, 0, WINDOW)
        latest = get_json(LATEST_CANDLE_KEY)
        bba = get_json(BEST_BID_ASK_KEY)

        feats, calib = compute_features(candles, latest, bba, window=WINDOW)
        if feats:
            set_json(FEATURE_KEY, feats)
        if calib:
            set_json(CALIB_KEY, calib)

        await asyncio.sleep(1)
