import json, redis

r = redis.Redis.from_url("redis://redis:6379/0", decode_responses=True)

def get_json(key):
    v = r.get(key)
    return json.loads(v) if v else None
