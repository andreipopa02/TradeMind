from typing import Optional, Dict, List
from pydantic import BaseModel, validator
from datetime import datetime


class BacktestDTO(BaseModel):
    id: Optional[int]
    user_id: int
    strategy_id: Optional[int]

    symbol: str
    time_frame: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]

    initial_balance: Optional[float]
    risk_per_trade: Optional[float]

    total_profit: Optional[float]
    drawdown_max: Optional[float]
    winrate: Optional[float]
    nr_trades: Optional[int]
    profit_factor: Optional[float]
    expectancy: Optional[float]
    balance_curve: Optional[List[Dict[str, float]]] = None

    created_at: Optional[datetime]
    name: Optional[str]

    class Config:
        from_attributes = True

    @validator("start_date", "end_date", pre=True)
    def parse_datetime(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return datetime.strptime(value, "%Y-%m-%d")
        return value