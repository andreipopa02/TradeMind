from typing import List, Optional

from business.bto.statistic_bto import StatisticBTO


class StatisticBAOInterface:
    def create_statistic(self, bto: StatisticBTO) -> StatisticBTO:
        pass

    def delete_statistic(self, statistic_id: int) -> bool:
        pass


    def get_statistic_by_id(self, statistic_id: int) -> Optional[StatisticBTO]:
        pass

    def get_statistics_by_user(self, user_id: int) -> List[StatisticBTO]:
        pass


    def generate_statistics(self, bto: StatisticBTO) -> dict:
        pass

    def update_statistic(self, statistic_id: int, updated_bto: StatisticBTO) -> Optional[StatisticBTO]:
        pass
