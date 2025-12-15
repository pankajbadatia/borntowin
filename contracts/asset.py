from pydantic import BaseModel

class AssetContext(BaseModel):
    symbol: str
    min_qty: float
    max_position: float
