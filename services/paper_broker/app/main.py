from fastapi import FastAPI, HTTPException, Query
from contracts.decision import TradeDecision
from app.broker import PaperBroker
from app.redis_store import get_json
from app.risk_engine import check_risk

app = FastAPI()
broker = PaperBroker()


@app.post("/execute")
def execute_trade(
    decision: TradeDecision,
    price: float = Query(..., gt=0)
):
    # --------------------------------------------------
    # 1️⃣ GLOBAL SAFETY GATE — TradePermission (Redis)
    # --------------------------------------------------
    permission = get_json("trade:permission")

    if not permission or not permission.get("allowed"):
        reason = permission.get("reason") if permission else "Trade permission unavailable"
        return {
            "status": "REJECTED",
            "reason": f"TradePermission: {reason}"
        }

    # --------------------------------------------------
    # 2️⃣ LOCAL RISK ENGINE — Position / Symbol rules
    # --------------------------------------------------
    risk = check_risk(decision, broker.position)
    if not risk.allowed:
        return {
            "status": "REJECTED",
            "reason": f"RiskEngine: {risk.reason}"
        }

    # --------------------------------------------------
    # 3️⃣ EXECUTION — State mutation happens ONLY here
    # --------------------------------------------------
    try:
        broker.execute(decision, price)

        return {
            "status": "FILLED",
            "position": {
                "qty": broker.position.qty,
                "avg_price": broker.position.avg_price,
            },
            "pnl": {
                "realized": broker.pnl.realized,
                "unrealized": 0.0,
            },
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
