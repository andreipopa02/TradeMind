from typing import List, Optional, Dict
from business.bal.statistic_bal import StatisticBAL
from business.bto.statistic_bto import StatisticBTO
from presentation.pao.interfaces.statistic_pao_interface import StatisticPAOInterface


class StatisticPAOService(StatisticPAOInterface):
    def __init__(self, statistic_bal: StatisticBAL):
        self.bal = statistic_bal


    def request_to_bto(self, data: Dict) -> StatisticBTO:
        if "user_id" not in data or "name" not in data:
            raise ValueError("Missing required fields: 'user_id' and 'name' are required.")

        return StatisticBTO(
            id=None,
            user_id=data["user_id"],
            name=data["name"],
            params=data.get("params"),
            is_active=data.get("is_active", True),
            created_at=None,
            updated_at=None
        )

    def bto_to_response(self, bto: StatisticBTO) -> Dict:
        return {
            "id": bto.id,
            "user_id": bto.user_id,
            "name": bto.name,
            "params": bto.params,
            "is_active": bto.is_active,
            "created_at": bto.created_at,
            "updated_at": bto.updated_at
        }


    def create_statistic(self, data: Dict) -> Dict:
        bto = self.request_to_bto(data)
        created = self.bal.create_statistic(bto)
        return self.bto_to_response(created)

    def get_statistic_by_id(self, statistic_id: int) -> Optional[Dict]:
        bto = self.bal.get_statistic_by_id(statistic_id)
        return self.bto_to_response(bto) if bto else None

    def get_statistics_by_user(self, user_id: int) -> List[Dict]:
        stats = self.bal.get_statistics_by_user(user_id)
        return [self.bto_to_response(stat) for stat in stats]

    def update_statistic(self, statistic_id: int, data: Dict) -> Optional[Dict]:
        bto = self.request_to_bto(data)
        updated = self.bal.update_statistic(statistic_id, bto)
        return self.bto_to_response(updated) if updated else None

    def delete_statistic(self, statistic_id: int) -> bool:
        return self.bal.delete_statistic(statistic_id)

    def generate_statistics(self, data: Dict) -> Dict:
        bto = self.request_to_bto(data)
        return self.bal.generate_statistics(bto)
