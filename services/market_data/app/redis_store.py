import os
import redis
import json
import time

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def set_json(key, value):
    r.set(key, json.dumps(value))

def get_json(key):
    v = r.get(key)
    return json.loads(v) if v else None

def update_data_status(**kwargs):
    status = get_json("market:data_status") or {}
    status.update(kwargs)
    status["updated_at"] = int(time.time())
    set_json("market:data_status", status)


def lpush_json(key, value, max_len=500):
    r.lpush(key, json.dumps(value))
    r.ltrim(key, 0, max_len - 1)
