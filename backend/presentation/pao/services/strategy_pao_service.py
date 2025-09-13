from typing import List, Optional, Dict
from business.bal.strategy_bal import StrategyBAL
from business.bto.strategy_bto import StrategyBTO
from presentation.pao.interfaces.strategy_pao_interface import StrategyPAOInterface

class StrategyPAOService(StrategyPAOInterface):
    def __init__(self, strategy_bal: StrategyBAL):
        self.bal = strategy_bal

    def request_to_bto(self, data: Dict) -> StrategyBTO:
        if "created_by" not in data or "name" not in data or "parameters" not in data:
            raise ValueError("Missing required fields: 'user_id', 'name' and 'code' are required.")

        return StrategyBTO(
            id=None,
            name=data["name"],
            type=data["type"],
            description=data["description"],
            parameters=data["parameters"],
            is_public=data.get("is_public", False),
            created_by=data["created_by"],
            created_at=None,
        )

    def bto_to_response(self, bto: StrategyBTO) -> Dict:
        return {
            "id": bto.id,
            "name": bto.name,
            "type": bto.type,
            "description": bto.description,
            "parameters": bto.parameters,
            "is_public": bto.is_public,
            "created_by": bto.created_by,
            "created_at": bto.created_at
        }

    def create_strategy(self, data: Dict) -> Dict:
        bto = self.request_to_bto(data)
        created = self.bal.create_strategy(bto)
        return self.bto_to_response(created)

    def get_strategy_by_id(self, strategy_id: int) -> Optional[Dict]:
        bto = self.bal.get_strategy_by_id(strategy_id)
        return self.bto_to_response(bto) if bto else None

    def get_strategies_by_user(self, user_id: int) -> List[Dict]:
        strategies = self.bal.get_strategies_by_user(user_id)
        return [self.bto_to_response(s) for s in strategies]

    def get_public_strategies(self) -> List[Dict]:
        strategies = self.bal.get_public_strategies()
        return [self.bto_to_response(s) for s in strategies]

    def get_public_strategy_by_type(self, strategy_type: str) -> Optional[Dict]:
        from persistence.entities.utils_entity import StrategyType
        try:
            strategy_type_enum = StrategyType(strategy_type)
        except ValueError:
            raise ValueError(f"Invalid strategy type: {strategy_type}")

        bto = self.bal.get_public_strategy_by_type(strategy_type_enum)
        return self.bto_to_response(bto) if bto else None

    def update_strategy(self, strategy_id: int, data: Dict) -> Optional[Dict]:
        bto = self.request_to_bto(data)
        updated = self.bal.update_strategy(strategy_id, bto)
        return self.bto_to_response(updated) if updated else None

    def delete_strategy(self, strategy_id: int) -> bool:
        return self.bal.delete_strategy(strategy_id)
