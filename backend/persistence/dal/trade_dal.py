from sqlalchemy.orm import Session
from typing import List, Optional

from persistence.dto.trade_dto import TradeDTO
from persistence.dao.repositories.trade_repository import TradeRepository
from persistence.entities.utils_entity import SourceType


class TradeDAL:
    def __init__(self, db: Session):
        self.repo = TradeRepository(db)


    # Create & Delete
    def add_trade(self, trade_dto: TradeDTO, user_id: int) -> TradeDTO:
        return self.repo.add_trade(trade_dto, user_id)

    def delete_trade(self, trade_id: int) -> bool:
        return self.repo.delete_trade(trade_id)


    # Setters
    def update_trade(self, trade_id: int, updated_trade_dto: TradeDTO) -> Optional[TradeDTO]:
        return self.repo.update_trade(trade_id, updated_trade_dto)


    # Getters
    def get_trade_by_id(self, trade_id: int) -> Optional[TradeDTO]:
        return self.repo.get_trade_by_id(trade_id)

    def get_trades_by_source(self, user_id: int, source: SourceType) -> List[TradeDTO]:
        return self.repo.get_trades_by_source(user_id, source)

    def get_trades_by_field(self, user_id: int, source: Optional[SourceType] = None, **filters) -> List[TradeDTO]:
        return self.repo.get_trades_by_field(user_id, source, **filters)

    def get_trades_by_backtest(self, backtest_id: int) -> List[TradeDTO]:
        return self.repo.get_trades_by_backtest(backtest_id)