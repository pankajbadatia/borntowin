from pydantic import BaseModel

class TradePermission(BaseModel):
    allowed: bool
    reason: str
