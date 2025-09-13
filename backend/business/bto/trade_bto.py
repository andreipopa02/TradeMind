from datetime import time, date
from typing import Optional

from persistence.entities.utils_entity import TradeType, SourceType, SessionType


class TradeBTO:
    def __init__(self,
                 id:            Optional[int],
                 user_id:       int,

                 market:        str,
                 volume:        float,
                 type:          TradeType,

                 open_date:     date,
                 open_time:     time,
                 close_date:    Optional[date] = None,
                 close_time:    Optional[time] = None,
                 session:       SessionType = SessionType.UNKNOWN,

                 open_price:    float = None,
                 close_price:   Optional[float] = None,
                 sl_price:      Optional[float] = None,
                 tp_price:      Optional[float] = None,

                 swap:          Optional[float] = None,
                 commission:    Optional[float] = None,
                 profit:        Optional[float] = None,
                 pips:          Optional[float] = None,

                 link_photo:    Optional[str] = None,

                 source_type:   SourceType = SourceType.UNKNOWN,
                 backtest_id:   Optional[int] = None
                 ):

        self.id         = id
        self.user_id    = user_id

        self.market     = market
        self.volume     = volume
        self.type       = type

        self.open_date  = open_date
        self.open_time = open_time
        self.close_date = close_date
        self.close_time = close_time
        self.session = session

        self.open_price = open_price
        self.close_price = close_price
        self.sl_price = sl_price
        self.tp_price = tp_price

        self.swap = swap
        self.commission = commission
        self.profit = profit
        self.pips = pips

        self.link_photo = link_photo

        self.source_type = source_type
        self.backtest_id = backtest_id






