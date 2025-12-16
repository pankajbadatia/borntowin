from app.state import PositionState, PnLState
from contracts.decision import TradeDecision


class PaperBroker:
    def __init__(self):
        self.position = PositionState()
        self.pnl = PnLState()

    def execute(self, decision: TradeDecision, price: float):
        if decision.action == "BUY":
            self._buy(decision.quantity, price)

        elif decision.action == "SELL":
            self._sell(decision.quantity, price)

        else:
            raise ValueError("Unknown action")

    def _buy(self, qty: float, price: float):
        """
        Spot BUY:
        - increase position
        - update weighted average price
        """
        if qty <= 0:
            raise ValueError("Buy quantity must be positive")

        # New total quantity
        new_qty = self.position.qty + qty

        # Weighted average price
        if self.position.qty == 0:
            new_avg = price
        else:
            total_cost = (self.position.qty * self.position.avg_price) + (qty * price)
            new_avg = total_cost / new_qty

        self.position.qty = new_qty
        self.position.avg_price = new_avg

    def _sell(self, qty: float, price: float):
        """
        Spot SELL:
        - cannot sell more than current position
        - realizes PnL
        """
        if qty <= 0:
            raise ValueError("Sell quantity must be positive")

        if self.position.qty <= 0:
            raise ValueError("No position to sell")

        if qty > self.position.qty:
            raise ValueError("Cannot sell more than current position")

        # Realized PnL
        realized = (price - self.position.avg_price) * qty
        self.pnl.realized += realized

        # Reduce position
        remaining_qty = self.position.qty - qty

        if remaining_qty == 0:
            # Flat position
            self.position.qty = 0.0
            self.position.avg_price = 0.0
        else:
            self.position.qty = remaining_qty
            # avg_price remains unchanged
