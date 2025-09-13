from typing import List, Optional

from business.bto.trade_bto import TradeBTO
from persistence.entities.utils_entity import SourceType


class TradeBAOInterface:
    def add_trade(self, trade_bto: TradeBTO) -> TradeBTO:
        pass

    def update_trade(self, trade_id: int, updated_trade_bto: TradeBTO) -> Optional[TradeBTO]:
        pass

    def delete_trade(self, trade_id: int) -> bool:
        pass

    def get_trades_by_field(self, user_id: int, source: Optional[SourceType] = None, **filters) -> List[TradeBTO]:
        pass

    def get_trades_by_user(self, user_id: int) -> List[TradeBTO]:
        pass

    def get_trades_by_backtest(self, backtest_id: int) -> List[TradeBTO]:
        pass