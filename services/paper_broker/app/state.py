from dataclasses import dataclass

@dataclass
class PositionState:
    qty: float = 0.0
    avg_price: float = 0.0

@dataclass
class PnLState:
    realized: float = 0.0
    unrealized: float = 0.0
