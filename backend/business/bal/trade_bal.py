from typing import List, Optional

from business.bto.trade_bto import TradeBTO
from business.bao.services.trade_bao_service import TradeBAOService
from persistence.entities.utils_entity import SourceType


class TradeBAL:
    def __init__(self, trade_bao: TradeBAOService):
        self.bao = trade_bao

    def add_trade(self, trade_bto: TradeBTO) -> TradeBTO:
        return self.bao.add_trade(trade_bto)

    def update_trade(self, trade_id: int, updated_trade_bto: TradeBTO) -> Optional[TradeBTO]:
        return self.bao.update_trade(trade_id, updated_trade_bto)

    def delete_trade(self, trade_id: int) -> bool:
        return self.bao.delete_trade(trade_id)

    def get_trades_by_field(self, user_id: int, source: Optional[SourceType] = None, **filters) -> List[TradeBTO]:
        return self.bao.get_trades_by_field(user_id, source, **filters)

    def get_trades_by_user(self, user_id: int) -> List[TradeBTO]:
        return self.bao.get_trades_by_user(user_id)

    def get_trades_by_backtest(self, backtest_id: int) -> List[TradeBTO]:
        return self.bao.get_trades_by_backtest(backtest_id)
