from typing import List, Optional
from business.bao.services.strategy_bao_service import StrategyBAOService
from business.bto.strategy_bto import StrategyBTO
from persistence.entities.utils_entity import StrategyType


class StrategyBAL:
    def __init__(self, service: StrategyBAOService):
        self.service = service

    def create_strategy(self, bto: StrategyBTO) -> StrategyBTO:
        return self.service.create_strategy(bto)

    def get_strategy_by_id(self, strategy_id: int) -> Optional[StrategyBTO]:
        return self.service.get_strategy_by_id(strategy_id)

    def get_strategies_by_user(self, user_id: int) -> List[StrategyBTO]:
        return self.service.get_strategies_by_user(user_id)

    def get_public_strategies(self) -> List[StrategyBTO]:
        return self.service.get_public_strategies()

    def update_strategy(self, strategy_id: int, updated_bto: StrategyBTO) -> Optional[StrategyBTO]:
        return self.service.update_strategy(strategy_id, updated_bto)

    def get_public_strategy_by_type(self, type: StrategyType) -> Optional[StrategyBTO]:
        return self.service.get_public_strategy_by_type(type)

    def get_strategy_by_type(self, type: StrategyType) -> Optional[StrategyBTO]:
        return self.service.get_strategy_by_type(type)

    def delete_strategy(self, strategy_id: int) -> bool:
        return self.service.delete_strategy(strategy_id)
