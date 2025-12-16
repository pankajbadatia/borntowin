from app.rules import (
    check_data_fresh,
    check_features,
    check_rvol,
    check_spread
)

def evaluate(data_status, features, calib):
    checks = {}

    ok, msg = check_data_fresh(data_status)
    checks["data_fresh"] = ok
    if not ok:
        return False, msg, checks

    ok, msg = check_features(features)
    checks["features_ready"] = ok
    if not ok:
        return False, msg, checks

    ok, msg = check_rvol(features, calib)
    checks["rvol_ok"] = ok
    if not ok:
        return False, msg, checks

    ok, msg = check_spread(features)
    checks["spread_ok"] = ok
    if not ok:
        return False, msg, checks

    return True, "OK", checks
