from typing import List, Optional, Dict

class StrategyPAOInterface:
    def create_strategy(self, data: Dict) -> Dict:
        pass

    def get_strategy_by_id(self, strategy_id: int) -> Optional[Dict]:
        pass

    def get_strategies_by_user(self, user_id: int) -> List[Dict]:
        pass

    def get_public_strategies(self) -> List[Dict]:
        pass

    def get_public_strategy_by_type(self, strategy_type: str) -> Optional[Dict]:
        pass

    def update_strategy(self, strategy_id: int, data: Dict) -> Optional[Dict]:
        pass

    def delete_strategy(self, strategy_id: int) -> bool:
        pass
