from typing import List, Optional, Dict
from presentation.pao.services.backtest_pao_service import BacktestPAOService

class BacktestPAL:
    def __init__(self, pao: BacktestPAOService):
        self.pao = pao

    def save_backtest(self, data: Dict) -> Dict:
        return self.pao.save_backtest(data)

    def run_backtest_preview(self, data: Dict) -> dict:
        return self.pao.run_backtest_preview(data)

    def get_backtest_by_id(self, backtest_id: int) -> Optional[Dict]:
        return self.pao.get_backtest_by_id(backtest_id)

    def get_backtests_by_user(self, user_id: int) -> List[Dict]:
        return self.pao.get_backtests_by_user(user_id)

    def get_backtests_by_strategy(self, strategy_id: int) -> List[Dict]:
        return self.pao.get_backtests_by_strategy(strategy_id)

    def delete_backtest(self, backtest_id: int) -> bool:
        return self.pao.delete_backtest(backtest_id)
