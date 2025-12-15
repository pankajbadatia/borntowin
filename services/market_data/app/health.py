# health.py
import time
from app.redis_store import get_json, update_data_status

def check_staleness(threshold):
    status = get_json("market:data_status")
    if not status:
        return

    now = int(time.time())
    last = status.get("last_trade_ts", 0)

    if now - last > threshold:
        update_data_status(stale=True)
