from app.state import PositionState, PnLState

class PaperBroker:
    def __init__(self):
        self.position = PositionState()
        self.pnl = PnLState()

    def execute(self, decision, price):
        if decision.action == "BUY":
            self._buy(decision.quantity, price)

        elif decision.action == "SELL":
            self._sell(decision.quantity, price)

    def _buy(self, qty, price):
        total_cost = self.position.avg_price * self.position.qty + price * qty
        self.position.qty += qty
        self.position.avg_price = total_cost / self.position.qty

    def _sell(self, qty, price):
        realized = qty * (price - self.position.avg_price)
        self.pnl.realized += realized
        self.position.qty -= qty
