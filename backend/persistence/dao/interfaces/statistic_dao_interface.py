from typing import List, Optional

from persistence.dto.statistic_dto import StatisticDTO


class StatisticDAOInterface:

    # Create & Delete
    def add_statistic(self, dto: StatisticDTO, user_id: int) -> StatisticDTO:
        pass

    def delete_statistic(self, statistic_id: int) -> bool:
        pass


    # Getters
    def get_statistic_by_id(self, statistic_id: int) -> Optional[StatisticDTO]:
        pass

    def get_statistics_by_user(self, user_id: int) -> List[StatisticDTO]:
        pass


    # Setters
    def update_statistic(self, statistic_id: int, updated_dto: StatisticDTO) -> Optional[StatisticDTO]:
        pass
