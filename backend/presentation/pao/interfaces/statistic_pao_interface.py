from typing import List, Optional, Dict


class StatisticPAOInterface:
    def create_statistic(self, data: Dict) -> Dict:
        pass

    def get_statistic_by_id(self, statistic_id: int) -> Optional[Dict]:
        pass

    def get_statistics_by_user(self, user_id: int) -> List[Dict]:
        pass

    def update_statistic(self, statistic_id: int, data: Dict) -> Optional[Dict]:
        pass

    def delete_statistic(self, statistic_id: int) -> bool:
        pass

    def generate_statistics(self, data: Dict) -> Dict:
        pass
