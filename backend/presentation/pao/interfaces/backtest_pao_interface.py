from typing import List, Optional, Dict

class BacktestPAOInterface:
    def save_backtest(self, data: Dict) -> Dict:
        pass

    def get_backtest_by_id(self, backtest_id: int) -> Optional[Dict]:
        pass

    def get_backtests_by_user(self, user_id: int) -> List[Dict]:
        pass

    def get_backtests_by_strategy(self, strategy_id: int) -> List[Dict]:
        pass

    def delete_backtest(self, backtest_id: int) -> bool:
        pass
