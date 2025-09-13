from pydantic import BaseModel
from typing import Optional


class TradingAccountDTO(BaseModel):
    id:             Optional[int]
    user_id :       int

    broker_name:    str
    account_id:     int
    server:         Optional[str]
    password:       str

    class Config:
        from_attributes = True
