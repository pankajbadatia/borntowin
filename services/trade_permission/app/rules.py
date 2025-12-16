import time

MAX_SPREAD_PCT = 0.002        # 0.20%
MIN_RVOL_FACTOR = 0.7        # relative to p70
STALE_SECONDS = 120          # data freshness window


def check_data_fresh(data_status):
    """
    Market data freshness is DERIVED from updated_at.
    Never trust persisted 'stale'.
    """
    if not data_status:
        return False, "Missing market data status"

    updated_at = data_status.get("updated_at")
    if not updated_at:
        return False, "Missing market heartbeat"

    now = int(time.time())
    if now - int(updated_at) > STALE_SECONDS:
        return False, "Market data stale"

    return True, "OK"


def check_features(features):
    if not features:
        return False, "Features not ready"
    return True, "OK"


def check_rvol(features, calib):
    """
    RVOL gating with calibration warm-up support.
    """
    rvol = features.get("rvol")
    if rvol is None:
        return False, "RVOL missing"

    # Calibration warming up → DO NOT BLOCK
    if not calib or calib.get("rvol_p70") is None:
        return True, "RVOL calibration warming up"

    return (
        rvol >= MIN_RVOL_FACTOR * calib["rvol_p70"],
        "RVOL below threshold"
    )


def check_spread(features):
    spread = features.get("spread_pct")

    # Spread data optional for now
    if spread is None:
        return True, "No spread data"

    return spread <= MAX_SPREAD_PCT, "Spread too wide"
