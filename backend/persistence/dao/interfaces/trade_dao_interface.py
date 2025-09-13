from typing import List, Optional

from persistence.dto.trade_dto import TradeDTO
from persistence.entities.utils_entity import SourceType


class TradeDAOInterface:

    # Create & Delete
    def add_trade(self, trade_dto: TradeDTO, user_id: int) -> TradeDTO:
        pass

    def delete_trade(self, trade_id: int) -> bool:
        pass


    # Getters
    def get_trade_by_id(self, trade_id: int) -> Optional[TradeDTO]:
        pass

    def get_trades_by_backtest_id(self, user_id: int, backtest_id: int) -> List[TradeDTO]:
        pass

    def get_trades_by_source(self, user_id: int, source: SourceType) -> List[TradeDTO]:
        pass

    def get_trades_by_field(self, user_id: int, source: Optional[SourceType] = None, **filters) -> List[TradeDTO]:
        pass

    def get_trades_by_backtest(self, backtest_id: int) -> List[TradeDTO]:
       pass

    # Setters
    def update_trade(self, trade_id: int, updated_trade_dto: TradeDTO) -> Optional[TradeDTO]:
        pass
