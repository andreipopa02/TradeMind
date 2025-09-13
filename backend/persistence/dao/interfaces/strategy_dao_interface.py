from typing import List, Optional
from persistence.dto.strategy_dto import StrategyDTO
from persistence.entities.utils_entity import StrategyType


class StrategyDAOInterface:

    # Create & Delete
    def add_strategy(self, dto: StrategyDTO, user_id: int) -> StrategyDTO:
        pass

    def delete_strategy(self, strategy_id: int) -> bool:
        pass


    # Getters
    def get_strategy_by_id(self, strategy_id: int) -> Optional[StrategyDTO]:
        pass

    def get_strategies_by_user(self, user_id: int) -> List[StrategyDTO]:
        pass

    def get_public_strategies(self) -> List[StrategyDTO]:
        pass

    def get_strategies_by_type(self, type: StrategyType) -> List[StrategyDTO]:
        pass

    def get_public_strategy_by_type(self, type: StrategyType) -> Optional[StrategyDTO]:
        pass

    # Setters
    def update_strategy(self, strategy_id: int, updated_dto: StrategyDTO) -> Optional[StrategyDTO]:
        pass
