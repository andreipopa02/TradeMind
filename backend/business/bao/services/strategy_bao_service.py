from typing import List, Optional
from sqlalchemy.orm import Session

from business.bao.interfaces.strategy_bao_interface import StrategyBAOInterface
from business.bto.strategy_bto import StrategyBTO
from business.mappers.strategy_mapper import StrategyMapper
from persistence.dal.strategy_dal import StrategyDAL
from persistence.entities.utils_entity import StrategyType
from persistence.utils.data_validators import validate_strategy_name, validate_strategy_type, \
    validate_strategy_parameters, validate_strategy_description


class StrategyBAOService(StrategyBAOInterface):
    def __init__(self, db: Session, strategy_dal: StrategyDAL):
        self.dal = strategy_dal

    def create_strategy(self, bto: StrategyBTO) -> StrategyBTO:
        validate_strategy_name(bto.name)
        validate_strategy_description(bto.description)
        validate_strategy_type(bto.type)
        validate_strategy_parameters(bto.parameters)

        dto = StrategyMapper.bto_to_dto(bto)
        saved_dto = self.dal.add_strategy(dto, user_id=bto.created_by)
        return StrategyMapper.dto_to_bto(saved_dto)

    def delete_strategy(self, strategy_id: int) -> bool:
        return self.dal.delete_strategy(strategy_id)

    def get_strategy_by_id(self, strategy_id: int) -> Optional[StrategyBTO]:
        dto = self.dal.get_strategy_by_id(strategy_id)
        return StrategyMapper.dto_to_bto(dto) if dto else None

    def get_strategies_by_user(self, user_id: int) -> List[StrategyBTO]:
        dtos = self.dal.get_strategies_by_user(user_id)
        return [StrategyMapper.dto_to_bto(dto) for dto in dtos]

    def get_public_strategies(self) -> List[StrategyBTO]:
        dtos = self.dal.get_public_strategies()
        return [StrategyMapper.dto_to_bto(dto) for dto in dtos]

    def get_public_strategy_by_type(self, type: StrategyType) -> Optional[StrategyBTO]:
        dto = self.dal.get_public_strategy_by_type(type)
        return StrategyMapper.dto_to_bto(dto) if dto else None

    def get_strategy_by_type(self, type: StrategyType) -> Optional[StrategyBTO]:
        dto_list = self.dal.get_public_strategies()
        for dto in dto_list:
            if dto.type == type:
                return StrategyMapper.dto_to_bto(dto)
        return None

    def update_strategy(self, strategy_id: int, updated_bto: StrategyBTO) -> Optional[StrategyBTO]:
        updated_dto = StrategyMapper.bto_to_dto(updated_bto)
        result_dto = self.dal.update_strategy(strategy_id, updated_dto)
        return StrategyMapper.dto_to_bto(result_dto) if result_dto else None
