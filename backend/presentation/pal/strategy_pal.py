from typing import List, Optional, Dict
from presentation.pao.services.strategy_pao_service import StrategyPAOService

class StrategyPAL:
    def __init__(self, pao: StrategyPAOService):
        self.pao = pao

    def create_strategy(self, data: Dict) -> Dict:
        return self.pao.create_strategy(data)

    def get_strategy_by_id(self, strategy_id: int) -> Optional[Dict]:
        return self.pao.get_strategy_by_id(strategy_id)

    def get_strategies_by_user(self, user_id: int) -> List[Dict]:
        return self.pao.get_strategies_by_user(user_id)

    def get_public_strategies(self) -> List[Dict]:
        return self.pao.get_public_strategies()

    def get_public_strategy_by_type(self, strategy_type: str) -> Optional[Dict]:
        return self.pao.get_public_strategy_by_type(strategy_type)

    def update_strategy(self, strategy_id: int, data: Dict) -> Optional[Dict]:
        return self.pao.update_strategy(strategy_id, data)

    def delete_strategy(self, strategy_id: int) -> bool:
        return self.pao.delete_strategy(strategy_id)
