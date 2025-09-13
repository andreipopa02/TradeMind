from typing import List

from presentation.pao.services.trade_pao_service import TradePAOService
from persistence.entities.utils_entity import SourceType


class TradePAL:
    def __init__(self, trade_pao: TradePAOService):
        self.pao = trade_pao

    def add_trade(self, trade_data: dict) -> dict:
        return self.pao.add_trade(trade_data)

    def update_trade(self, trade_id: int, updated_trade_data: dict) -> dict:
        return self.pao.update_trade(trade_id, updated_trade_data)

    def delete_trade(self, trade_id: int) -> bool:
        return self.pao.delete_trade(trade_id)

    def get_trades_by_field(self, user_id: int, source: SourceType, **filters) -> List[dict]:
        return self.pao.get_trades_by_field(user_id, source, filters)

    def get_trades_by_user(self, user_id: int) -> List[dict]:
        return self.pao.get_trades_by_user(user_id)

    def get_trades_by_backtest(self, backtest_id: int) -> List[dict]:
        return self.pao.get_trades_by_backtest(backtest_id)
