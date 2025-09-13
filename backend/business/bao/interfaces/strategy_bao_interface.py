from typing import List, Optional
from business.bto.strategy_bto import StrategyBTO
from persistence.entities.utils_entity import StrategyType


class StrategyBAOInterface:
    def create_strategy(self, bto: StrategyBTO) -> StrategyBTO:
        pass

    def delete_strategy(self, strategy_id: int) -> bool:
        pass

    def get_strategy_by_id(self, strategy_id: int) -> Optional[StrategyBTO]:
        pass

    def get_strategies_by_user(self, user_id: int) -> List[StrategyBTO]:
        pass

    def get_public_strategies(self) -> List[StrategyBTO]:
        pass

    def get_public_strategy_by_type(self, type: StrategyType) -> Optional[StrategyBTO]:
        pass

    def get_strategy_by_type(self, type: StrategyType) -> Optional[StrategyBTO]:
        pass

    def update_strategy(self, strategy_id: int, updated_bto: StrategyBTO) -> Optional[StrategyBTO]:
        pass
