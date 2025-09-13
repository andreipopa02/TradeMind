from typing import List, Optional, Dict

from presentation.pao.services.statistic_pao_service import StatisticPAOService


class StatisticPAL:
    def __init__(self, pao: StatisticPAOService):
        self.pao = pao

    def create_statistic(self, data: Dict) -> Dict:
        return self.pao.create_statistic(data)

    def get_statistic_by_id(self, statistic_id: int) -> Optional[Dict]:
        return self.pao.get_statistic_by_id(statistic_id)

    def get_statistics_by_user(self, user_id: int) -> List[Dict]:
        return self.pao.get_statistics_by_user(user_id)

    def update_statistic(self, statistic_id: int, data: Dict) -> Optional[Dict]:
        return self.pao.update_statistic(statistic_id, data)

    def delete_statistic(self, statistic_id: int) -> bool:
        return self.pao.delete_statistic(statistic_id)

    def generate_statistics(self, data: Dict) -> Dict:
        return self.pao.generate_statistics(data)
