from typing import Optional
from pydantic import BaseModel
from datetime import date, time
from persistence.entities.utils_entity import TradeType, SourceType, SessionType


class TradeDTO(BaseModel):
    id:          Optional[int]
    user_id:     int

    market:      str
    volume:      float
    type:        TradeType

    open_date:   date
    open_time:   time
    close_date:  Optional[date]
    close_time:  Optional[time]
    session:     Optional[SessionType]

    open_price:  float
    close_price: Optional[float]
    sl_price:    Optional[float]
    tp_price:    Optional[float]

    swap:        Optional[float]
    commission:  Optional[float]
    profit:      Optional[float]
    pips:        Optional[float]

    link_photo:  Optional[str]

    source_type: SourceType
    backtest_id : Optional[int]

    class Config:
        from_attributes = True
