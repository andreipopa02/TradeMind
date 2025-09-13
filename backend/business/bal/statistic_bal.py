from typing import List, Optional

from business.bao.services.statistic_bao_service import StatisticBAOService
from business.bto.statistic_bto import StatisticBTO


class StatisticBAL:
    def __init__(self, service: StatisticBAOService):
        self.service = service

    def create_statistic(self, bto: StatisticBTO) -> StatisticBTO:
        return self.service.create_statistic(bto)

    def get_statistic_by_id(self, statistic_id: int) -> Optional[StatisticBTO]:
        return self.service.get_statistic_by_id(statistic_id)

    def get_statistics_by_user(self, user_id: int) -> List[StatisticBTO]:
        return self.service.get_statistics_by_user(user_id)

    def update_statistic(self, statistic_id: int, updated_bto: StatisticBTO) -> Optional[StatisticBTO]:
        return self.service.update_statistic(statistic_id, updated_bto)

    def delete_statistic(self, statistic_id: int) -> bool:
        return self.service.delete_statistic(statistic_id)

    def generate_statistics(self, bto: StatisticBTO) -> dict:
        return self.service.generate_statistics(bto)
