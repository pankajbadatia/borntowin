import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

CANDLE_LIST_KEY = "market:candles:1m:list"
LATEST_CANDLE_KEY = "market:candles:1m"
BEST_BID_ASK_KEY = "market:best_bid_ask"

FEATURE_KEY = "feature:latest"
CALIB_KEY = "feature:calibration"

WINDOW = int(os.getenv("FEATURE_WINDOW", "120"))

DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"
MIN_CANDLES = int(os.getenv("MIN_CANDLES", "10" if DEV_MODE else "20"))
