from contracts.risk import TradePermission
from app.settings import MAX_POSITION, SYMBOL

def check_risk(decision, position):
    if decision.symbol != SYMBOL:
        return TradePermission(allowed=False, reason="Symbol mismatch")
    
    if decision.action == "BUY":
        if position.qty + decision.quantity > MAX_POSITION:
            return TradePermission(allowed=False, reason="Max position exceeded")
        

    if decision.action == "SELL":
        if position.qty - decision.quantity < -MAX_POSITION:
            return TradePermission(allowed=False, reason="Short not allowed")


    return TradePermission(allowed=True, reason="OK")
