import json, redis, time
from pydantic import BaseModel
from typing import Dict

REDIS_URL = "redis://redis:6379/0"

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_json(key):
    v = r.get(key)
    return json.loads(v) if v else None

def set_json(key, value):
    value["ts"] = int(time.time())
    r.set(key, json.dumps(value))
