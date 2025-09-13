from sqlalchemy.orm import Session
from typing import List, Optional

from persistence.dao.interfaces.trade_dao_interface import TradeDAOInterface
from persistence.entities.trade_entity import TradeEntity
from persistence.dto.trade_dto import TradeDTO
from persistence.entities.utils_entity import SourceType
from persistence.mappers.trade_mapper import TradeMapper


class TradeRepository(TradeDAOInterface):
    def __init__(self, db: Session):
        self.db = db


    # Create & Delete
    def add_trade(self, trade_dto: TradeDTO, user_id: int) -> TradeDTO:
        try:
            trade_entity = TradeMapper.dto_to_entity(trade_dto)
            trade_entity.user_id = user_id

            self.db.add(trade_entity)
            self.db.commit()
            self.db.refresh(trade_entity)
            return TradeMapper.entity_to_dto(trade_entity)
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_trade(self, trade_id: int) -> bool:
        try:
            trade = self.db.query(TradeEntity).filter(TradeEntity.id == trade_id).first()
            if not trade:
                return False
            self.db.delete(trade)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e


    # Setters
    def update_trade(self, trade_id: int, updated_trade_dto: TradeDTO) -> Optional[TradeDTO]:
        try:
            trade = self.db.query(TradeEntity).filter(
                TradeEntity.id == trade_id
            ).first()

            if not trade:
                return None

            update_fields = {k: v for k, v in updated_trade_dto.dict().items() if
                             k not in ["id", "user_id", "source_type"] and v is not None}

            for key, value in update_fields.items():
                setattr(trade, key, value)

            self.db.commit()
            self.db.refresh(trade)
            return TradeMapper.entity_to_dto(trade)
        except Exception as e:
            self.db.rollback()
            raise e


    # Getters
    def get_trade_by_id(self, trade_id: int) -> Optional[TradeDTO]:
        try:
            trade = self.db.query(TradeEntity).filter(TradeEntity.id == trade_id).first()
            return TradeMapper.entity_to_dto(trade) if trade else None
        except Exception as e:
            self.db.rollback()
            raise e

    def get_trades_by_source(self, user_id: int, source_type: SourceType) -> List[TradeDTO]:
        try:
            trades = self.db.query(TradeEntity).filter(
                TradeEntity.user_id == user_id,
                TradeEntity.source_type == source_type
            ).all()
            return [TradeMapper.entity_to_dto(trade) for trade in trades]
        except Exception as e:
            self.db.rollback()
            raise e

    def get_trades_by_backtest(self, backtest_id: int) -> List[TradeDTO]:
        try:
            trades = self.db.query(TradeEntity).filter(
                TradeEntity.backtest_id == backtest_id,
                TradeEntity.source_type == SourceType.BACKTEST
            ).all()
            return [TradeMapper.entity_to_dto(trade) for trade in trades]
        except Exception as e:
            self.db.rollback()
            raise e

    def get_trades_by_field(self, user_id: int, source: Optional[SourceType] = None, **filters) -> List[TradeDTO]:
        try:
            query = self.db.query(TradeEntity).filter(TradeEntity.user_id == user_id)

            if source:
                query = query.filter(TradeEntity.source_type == source)

            for field, value in filters.items():
                if "__" in field:
                    attr_name, op = field.split("__", 1)
                    if not hasattr(TradeEntity, attr_name):
                        continue

                    column = getattr(TradeEntity, attr_name)

                    if op == "gte":
                        query = query.filter(column >= value)
                    elif op == "lte":
                        query = query.filter(column <= value)
                    elif op == "gt":
                        query = query.filter(column > value)
                    elif op == "lt":
                        query = query.filter(column < value)
                    elif op == "range" and isinstance(value, (tuple, list)) and len(value) == 2:
                        query = query.filter(column.between(value[0], value[1]))
                    elif op == "in" and isinstance(value, list):
                        query = query.filter(column.in_(value))
                    elif op == "neq":
                        query = query.filter(column != value)
                else:
                    if hasattr(TradeEntity, field):
                        column = getattr(TradeEntity, field)
                        if isinstance(value, list):
                            query = query.filter(column.in_(value))
                        else:
                            query = query.filter(column == value)

            trades = query.all()
            return [TradeMapper.entity_to_dto(trade) for trade in trades]

        except Exception as e:
            self.db.rollback()
            raise e
