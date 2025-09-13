from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class BacktestBTO:
    def __init__(self,
                 id: Optional[int],
                 user_id: int,
                 strategy_id: Optional[int],

                 symbol: str,
                 time_frame: str,
                 start_date: Optional[datetime] = None,
                 end_date: Optional[datetime] = None,

                 initial_balance: Optional[float] = None,
                 risk_per_trade: Optional[float] = None,
                 risk_reward_ratio: Optional[float] = None,

                 total_profit: Optional[float] = None,
                 drawdown_max: Optional[float] = None,
                 winrate: Optional[float] = None,
                 nr_trades: Optional[int] = None,
                 profit_factor: Optional[float] = None,
                 expectancy: Optional[float] = None,
                 balance_curve: Optional[List[Dict[str, float]]] = None,

                 created_at: Optional[datetime] = None,
                 name: Optional[str] = None
                 ):
        self.id = id
        self.user_id = user_id
        self.strategy_id = strategy_id

        self.symbol = symbol
        self.time_frame = time_frame
        self.start_date = start_date
        self.end_date = end_date

        self.initial_balance = initial_balance
        self.risk_per_trade = risk_per_trade
        self.risk_reward_ratio = risk_reward_ratio

        self.total_profit = total_profit
        self.drawdown_max = drawdown_max
        self.winrate = winrate
        self.nr_trades = nr_trades
        self.profit_factor = profit_factor
        self.expectancy = expectancy
        self.balance_curve = balance_curve

        self.created_at = created_at
        self.name = name

class BacktestRequestBTO(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    timeframe: str

class TradeBTO(BaseModel):
    trade_id: int
    action: str
    timestamp: datetime
    price: float
    profit: float

class CandleBTO(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float

class BacktestResultBTO(BaseModel):
    trades: List[TradeBTO]
    total_profit: float
    candles: List[CandleBTO]


