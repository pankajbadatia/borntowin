import numpy as np
from app.settings import MIN_CANDLES

def compute_features(candles_newest_first, latest_candle, best_bid_ask, window=120):
    # Need oldest->newest for math
    closed = list(reversed(candles_newest_first[:window]))
    # if len(closed) < 20 or not latest_candle:
    #     return None, None
    if len(closed) < MIN_CANDLES or not latest_candle:
        return None, None

    closes = np.array([c["close"] for c in closed], dtype=float)
    highs  = np.array([c["high"]  for c in closed], dtype=float)
    lows   = np.array([c["low"]   for c in closed], dtype=float)
    vols   = np.array([c["volume"] for c in closed], dtype=float)

    # log returns
    rets = np.diff(np.log(closes))
    ret_1m = float(rets[-1]) if len(rets) else 0.0
    ret_5m = float(np.sum(rets[-5:])) if len(rets) >= 5 else float(np.sum(rets))
    rv = float(np.std(rets[-30:]) * np.sqrt(30)) if len(rets) >= 30 else float(np.std(rets))

    # ATR (simple True Range on last 14)
    prev_close = np.roll(closes, 1)
    prev_close[0] = closes[0]
    tr = np.maximum(highs - lows, np.maximum(np.abs(highs - prev_close), np.abs(lows - prev_close)))
    atr = float(np.mean(tr[-14:])) if len(tr) >= 14 else float(np.mean(tr))
    atr_pct = float(atr / closes[-1]) if closes[-1] != 0 else 0.0

    # RVOL: current volume vs avg volume (last 30 closed candles)
    avg_vol = float(np.mean(vols[-30:])) if len(vols) >= 30 else float(np.mean(vols))
    cur_vol = float(latest_candle.get("volume", 0.0))
    rvol = float(cur_vol / avg_vol) if avg_vol > 0 else 0.0

    # Spread %
    spread_pct = None
    if best_bid_ask and best_bid_ask.get("bid") and best_bid_ask.get("ask"):
        bid = float(best_bid_ask["bid"]); ask = float(best_bid_ask["ask"])
        mid = (bid + ask) / 2.0
        spread_pct = float((ask - bid) / mid) if mid > 0 else None

    features = {
        "ret_1m": ret_1m,
        "ret_5m": ret_5m,
        "realized_vol_30m": rv,
        "atr_pct": atr_pct,
        "rvol": rvol,
        "spread_pct": spread_pct,
        "close": float(latest_candle["close"]),
        "ts": int(latest_candle["ts"]),
    }

    # calibration example: RVOL p70 from last 120 closed candles volumes
    # (simple proxy: volume/mean(volume))
    if len(vols) >= 50:
        vratio = vols / (np.mean(vols) + 1e-12)
        rvol_p70 = float(np.quantile(vratio, 0.70))
    else:
        rvol_p70 = None

    calib = {"rvol_p70": rvol_p70, "atr_pct_avg": float(np.mean(tr) / closes[-1])}

    return features, calib
