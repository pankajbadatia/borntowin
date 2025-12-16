import asyncio
from fastapi import FastAPI
from app.redis_store import get_json, set_json
from app.gate import evaluate

app = FastAPI()

@app.get("/permission")
def permission():
    return get_json("trade:permission") or {}

@app.on_event("startup")
async def startup():
    asyncio.create_task(loop())

async def loop():
    while True:
        data_status = get_json("market:data_status")
        features = get_json("feature:latest")
        calib = get_json("feature:calibration")

        allowed, reason, checks = evaluate(data_status, features, calib)

        set_json("trade:permission", {
            "allowed": allowed,
            "reason": reason,
            "checks": checks
        })

        await asyncio.sleep(1)
