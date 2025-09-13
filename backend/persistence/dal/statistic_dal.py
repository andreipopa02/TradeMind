from sqlalchemy.orm import Session
from typing import List, Optional

from persistence.dao.interfaces.statistic_dao_interface import StatisticDAOInterface
from persistence.dao.repositories.statistic_repository import StatisticRepository
from persistence.dto.statistic_dto import StatisticDTO


class StatisticDAL:
    def __init__(self, db: Session):
        self.repo = StatisticRepository(db)


    # Create & Delete
    def add_statistic(self, dto: StatisticDTO, user_id: int) -> StatisticDTO:
        return self.repo.add_statistic(dto, user_id)

    def delete_statistic(self, statistic_id: int) -> bool:
        return self.repo.delete_statistic(statistic_id)


    # Getters
    def get_statistic_by_id(self, statistic_id: int) -> Optional[StatisticDTO]:
        return self.repo.get_statistic_by_id(statistic_id)

    def get_statistics_by_user(self, user_id: int) -> List[StatisticDTO]:
        return self.repo.get_statistics_by_user(user_id)


    # Setters
    def update_statistic(self, statistic_id: int, updated_dto: StatisticDTO) -> Optional[StatisticDTO]:
        return self.repo.update_statistic(statistic_id, updated_dto)