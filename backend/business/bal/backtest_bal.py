from typing import List, Optional
from business.bao.services.backtest_bao_service import BacktestBAOService
from business.bto.backtest_bto import BacktestBTO

class BacktestBAL:
    def __init__(self, service: BacktestBAOService):
        self.service = service

    def save_backtest(self, bto: BacktestBTO, executed_trades: List[dict]) -> BacktestBTO:
        return self.service.save_backtest(bto, executed_trades)

    def run_backtest_preview(self, bto: BacktestBTO) -> dict:
        return self.service.run_backtest_preview(bto)

    def get_backtest_by_id(self, backtest_id: int) -> Optional[BacktestBTO]:
        return self.service.get_backtest_by_id(backtest_id)

    def get_backtests_by_user(self, user_id: int) -> List[BacktestBTO]:
        return self.service.get_backtests_by_user(user_id)

    def get_backtests_by_strategy(self, strategy_id: int) -> List[BacktestBTO]:
        return self.service.get_backtests_by_strategy(strategy_id)

    def update_backtest(self, backtest_id: int, updated_bto: BacktestBTO) -> Optional[BacktestBTO]:
        return self.service.update_backtest(backtest_id, updated_bto)

    def get_backtest_metrics(self, backtest_id: int) -> Optional[dict]:
        return self.service.get_backtest_metrics(backtest_id)

    def delete_backtest(self, backtest_id: int) -> bool:
        return self.service.delete_backtest(backtest_id)

    def update_backtest_metrics(self, backtest_id: int, metrics: dict) -> bool:
        return self.service.update_backtest_metrics(backtest_id, metrics)
