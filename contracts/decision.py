from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID
from datetime import datetime

class Action(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    NO_TRADE = "NO_TRADE"

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class TradeDecision(BaseModel):
    decision_id: UUID
    symbol: str
    action: Action
    order_type: OrderType
    quantity: float
    confidence: float = Field(ge=0, le=1)
    created_at: datetime
