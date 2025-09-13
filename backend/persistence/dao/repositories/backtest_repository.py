from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List, Optional
from persistence.dao.interfaces.backtest_dao_interface import BacktestDAOInterface
from persistence.entities.backtest_entity import BacktestEntity
from persistence.dto.backtest_dto import BacktestDTO
from persistence.mappers.backtest_mapper import BacktestMapper

class BacktestRepository(BacktestDAOInterface):
    def __init__(self, db: Session):
        self.db = db

    def add_backtest(self, dto: BacktestDTO, user_id: int) -> BacktestDTO:
        try:
            entity = BacktestMapper.dto_to_entity(dto)
            entity.user_id = user_id
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return BacktestMapper.entity_to_dto(entity)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete_backtest(self, backtest_id: int) -> bool:
        try:
            entity = self.db.query(BacktestEntity).filter(BacktestEntity.id == backtest_id).first()
            if not entity:
                return False
            self.db.delete(entity)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e


    def get_backtest_by_id(self, backtest_id: int) -> Optional[BacktestDTO]:
        entity = self.db.query(BacktestEntity).filter(BacktestEntity.id == backtest_id).first()
        return BacktestMapper.entity_to_dto(entity) if entity else None

    def get_backtests_by_user(self, user_id: int) -> List[BacktestDTO]:
        entities = self.db.query(BacktestEntity).filter(BacktestEntity.user_id == user_id).all()
        return [BacktestMapper.entity_to_dto(e) for e in entities]

    def get_backtests_by_strategy(self, strategy_id: int) -> List[BacktestDTO]:
        entities = self.db.query(BacktestEntity).filter(BacktestEntity.strategy_id == strategy_id).all()
        return [BacktestMapper.entity_to_dto(e) for e in entities]

    def get_backtest_metrics(self, backtest_id: int) -> Optional[dict]:
        entity = self.db.query(BacktestEntity).filter(BacktestEntity.id == backtest_id).first()
        if not entity:
            return None
        return {
            "initial_balance": entity.initial_balance,
            "risk_per_trade": entity.risk_per_trade,
            "total_profit": entity.total_profit,
            "drawdown_max": entity.drawdown_max,
            "winrate": entity.winrate,
            "nr_trades": entity.nr_trades,
            "profit_factor": entity.profit_factor,
            "expectancy": entity.expectancy,
            "balance_curve": entity.balance_curve,
        }


    def update_backtest(self, backtest_id: int, updated_dto: BacktestDTO) -> Optional[BacktestDTO]:
        try:
            backtest = self.db.query(BacktestEntity).filter(BacktestEntity.id == backtest_id).first()
            if not backtest:
                return None

            update_fields = {
                k: v for k, v in updated_dto.dict().items()
                if k not in ["id", "user_id"] and v is not None
            }

            for key, value in update_fields.items():
                setattr(backtest, key, value)

            self.db.commit()
            self.db.refresh(backtest)
            return BacktestMapper.entity_to_dto(backtest)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def update_backtest_metrics(self, backtest_id: int, metrics: dict) -> bool:
        try:
            backtest = self.db.query(BacktestEntity).filter(BacktestEntity.id == backtest_id).first()
            if not backtest:
                return False

            allowed_fields = [
                "initial_balance", "risk_per_trade", "total_profit", "drawdown_max", "winrate",
                "nr_trades", "profit_factor", "expectancy", "balance_curve"  ]

            for key, value in metrics.items():
                if key in allowed_fields:
                    setattr(backtest, key, value)

            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
