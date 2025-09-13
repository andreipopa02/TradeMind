from sqlalchemy.orm import Session
from typing import List, Optional
from persistence.dao.interfaces.strategy_dao_interface import StrategyDAOInterface
from persistence.dao.repositories.strategy_repository import StrategyRepository
from persistence.dto.strategy_dto import StrategyDTO
from persistence.entities.utils_entity import StrategyType


class StrategyDAL:
    def __init__(self, db: Session):
        self.repo: StrategyDAOInterface = StrategyRepository(db)

    def add_strategy(self, dto: StrategyDTO, user_id: int) -> StrategyDTO:
        return self.repo.add_strategy(dto, user_id)

    def delete_strategy(self, strategy_id: int) -> bool:
        return self.repo.delete_strategy(strategy_id)

    def get_strategy_by_id(self, strategy_id: int) -> Optional[StrategyDTO]:
        return self.repo.get_strategy_by_id(strategy_id)

    def get_strategies_by_user(self, user_id: int) -> List[StrategyDTO]:
        return self.repo.get_strategies_by_user(user_id)

    def get_public_strategies(self) -> List[StrategyDTO]:
        return self.repo.get_public_strategies()

    def get_public_strategy_by_type(self, type: StrategyType) -> Optional[StrategyDTO]:
        return self.repo.get_public_strategy_by_type(type)

    def get_strategies_by_type(self, type: StrategyType) -> List[StrategyDTO]:
        return self.repo.get_strategies_by_type(type)


    def update_strategy(self, strategy_id: int, updated_dto: StrategyDTO) -> Optional[StrategyDTO]:
        return self.repo.update_strategy(strategy_id, updated_dto)
