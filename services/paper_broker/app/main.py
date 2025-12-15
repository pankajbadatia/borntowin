from fastapi import FastAPI
from contracts.decision import TradeDecision

from app.broker import PaperBroker
from app.risk_engine import check_risk
from contracts.decision import TradeDecision

app = FastAPI()
broker = PaperBroker()

@app.post("/execute")
def execute_trade(decision: TradeDecision, price: float):
    permission = check_risk(decision, broker.position)
    if not permission.allowed:
        return {"status": "REJECTED", "reason": permission.reason}

    broker.execute(decision, price)
    return {
        "status": "FILLED",
        "position": broker.position,
        "pnl": broker.pnl
    }
