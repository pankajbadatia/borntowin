import json, redis
from app.settings import REDIS_URL

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_json(key):
    v = r.get(key)
    return json.loads(v) if v else None

def set_json(key, value):
    r.set(key, json.dumps(value))

def lrange_json(key, start=0, end=200):
    items = r.lrange(key, start, end)
    return [json.loads(x) for x in items]
