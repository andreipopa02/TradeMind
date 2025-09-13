from sqlalchemy.orm import Session
from typing import List, Optional
from persistence.dao.interfaces.backtest_dao_interface import BacktestDAOInterface
from persistence.dao.repositories.backtest_repository import BacktestRepository
from persistence.dto.backtest_dto import BacktestDTO

class BacktestDAL:
    def __init__(self, db: Session):
        self.repo: BacktestDAOInterface = BacktestRepository(db)

    def add_backtest(self, dto: BacktestDTO, user_id: int) -> BacktestDTO:
        return self.repo.add_backtest(dto, user_id)


    def delete_backtest(self, backtest_id: int) -> bool:
        return self.repo.delete_backtest(backtest_id)


    def get_backtest_by_id(self, backtest_id: int) -> Optional[BacktestDTO]:
        return self.repo.get_backtest_by_id(backtest_id)

    def get_backtests_by_user(self, user_id: int) -> List[BacktestDTO]:
        return self.repo.get_backtests_by_user(user_id)

    def get_backtests_by_strategy(self, strategy_id: int) -> List[BacktestDTO]:
        return self.repo.get_backtests_by_strategy(strategy_id)

    def get_backtest_metrics(self, backtest_id: int) -> Optional[dict]:
        return self.repo.get_backtest_metrics(backtest_id)


    def update_backtest(self, backtest_id: int, updated_dto: BacktestDTO) -> Optional[BacktestDTO]:
        return self.repo.update_backtest(backtest_id, updated_dto)

    def update_backtest_metrics(self, backtest_id: int, metrics: dict) -> bool:
        return self.repo.update_backtest_metrics(backtest_id, metrics)