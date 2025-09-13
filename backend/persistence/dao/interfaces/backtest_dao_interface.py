from typing import List, Optional
from persistence.dto.backtest_dto import BacktestDTO

class BacktestDAOInterface:

    # Create & Delete
    def add_backtest(self, dto: BacktestDTO, user_id: int) -> BacktestDTO:
        pass

    def delete_backtest(self, backtest_id: int) -> bool:
        pass


    # Getters
    def get_backtest_by_id(self, backtest_id: int) -> Optional[BacktestDTO]:
        pass

    def get_backtests_by_user(self, user_id: int) -> List[BacktestDTO]:
        pass

    def get_backtests_by_strategy(self, strategy_id: int) -> List[BacktestDTO]:
        pass

    def get_backtest_metrics(self, backtest_id: int) -> Optional[dict]:
        pass


    # Setters
    def update_backtest(self, backtest_id: int, updated_dto: BacktestDTO) -> Optional[BacktestDTO]:
        pass

    def update_backtest_metrics(self, backtest_id: int, metrics: dict) -> bool:
        pass
