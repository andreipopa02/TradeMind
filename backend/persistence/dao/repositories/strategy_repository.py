from sqlalchemy.orm import Session
from typing import List, Optional
from persistence.dao.interfaces.strategy_dao_interface import StrategyDAOInterface
from persistence.entities.strategy_entity import StrategyEntity
from persistence.dto.strategy_dto import StrategyDTO
from persistence.entities.utils_entity import StrategyType
from persistence.mappers.strategy_mapper import StrategyMapper


class StrategyRepository(StrategyDAOInterface):
    def __init__(self, db: Session):
        self.db = db

    def add_strategy(self, dto: StrategyDTO, user_id: int) -> StrategyDTO:
        entity = StrategyMapper.dto_to_entity(dto)
        entity.created_by = user_id
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return StrategyMapper.entity_to_dto(entity)

    def delete_strategy(self, strategy_id: int) -> bool:
        entity = self.db.query(StrategyEntity).filter(StrategyEntity.id == strategy_id).first()
        if not entity:
            return False
        self.db.delete(entity)
        self.db.commit()
        return True

    def get_strategy_by_id(self, strategy_id: int) -> Optional[StrategyDTO]:
        entity = self.db.query(StrategyEntity).filter(StrategyEntity.id == strategy_id).first()
        return StrategyMapper.entity_to_dto(entity) if entity else None

    def get_strategies_by_user(self, user_id: int) -> List[StrategyDTO]:
        entities = self.db.query(StrategyEntity).filter(StrategyEntity.created_by == user_id).all()
        return [StrategyMapper.entity_to_dto(e) for e in entities]

    def get_public_strategies(self) -> List[StrategyDTO]:
        entities = self.db.query(StrategyEntity).filter(StrategyEntity.is_public == True).all()
        return [StrategyMapper.entity_to_dto(e) for e in entities]

    def get_public_strategy_by_type(self, type: StrategyType) -> Optional[StrategyDTO]:
        entity = (
            self.db.query(StrategyEntity)
            .filter(StrategyEntity.type == type, StrategyEntity.is_public == True)
            .first()
        )
        return StrategyMapper.entity_to_dto(entity) if entity else None

    def get_strategies_by_type(self, type: StrategyType) -> List[StrategyDTO]:
        entities = self.db.query(StrategyEntity).filter(StrategyEntity.type == type).all()
        return [StrategyMapper.entity_to_dto(e) for e in entities]

    def strategy_name_exists(self, name: str) -> bool:
        return self.db.query(StrategyEntity).filter(StrategyEntity.name == name).first() is not None

    def update_strategy(self, strategy_id: int, updated_dto: StrategyDTO) -> Optional[StrategyDTO]:
        strategy = self.db.query(StrategyEntity).filter(StrategyEntity.id == strategy_id).first()
        if not strategy:
            return None

        update_fields = {
            k: v for k, v in updated_dto.dict().items()
            if k not in ["id", "created_by"] and v is not None
        }

        for key, value in update_fields.items():
            setattr(strategy, key, value)

        self.db.commit()
        self.db.refresh(strategy)
        return StrategyMapper.entity_to_dto(strategy)
