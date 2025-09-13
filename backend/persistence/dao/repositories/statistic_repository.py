from sqlalchemy.orm import Session
from typing import List, Optional

from persistence.dao.interfaces.statistic_dao_interface import StatisticDAOInterface
from persistence.entities.statistic_entity import StatisticEntity
from persistence.dto.statistic_dto import StatisticDTO
from persistence.mappers.statistic_mapper import StatisticMapper


class StatisticRepository(StatisticDAOInterface):
    def __init__(self, db: Session):
        self.db = db


    # Create & Delete
    def add_statistic(self, dto: StatisticDTO, user_id: int) -> StatisticDTO:
        entity = StatisticMapper.dto_to_entity(dto)
        entity.user_id = user_id

        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)

        return StatisticMapper.entity_to_dto(entity)

    def delete_statistic(self, statistic_id: int) -> bool:
        entity = self.db.query(StatisticEntity).filter(StatisticEntity.id == statistic_id).first()
        if not entity:
            return False

        self.db.delete(entity)
        self.db.commit()

        return True


    # Getters
    def get_statistic_by_id(self, statistic_id: int) -> Optional[StatisticDTO]:
        entity = self.db.query(StatisticEntity).filter(StatisticEntity.id == statistic_id).first()
        return StatisticMapper.entity_to_dto(entity) if entity else None

    def get_statistics_by_user(self, user_id: int) -> List[StatisticDTO]:
        entities = self.db.query(StatisticEntity).filter(StatisticEntity.user_id == user_id).all()
        return [StatisticMapper.entity_to_dto(e) for e in entities]


    # Setters
    def update_statistic(self, statistic_id: int, updated_dto: StatisticDTO) -> Optional[StatisticDTO]:
        statistic = self.db.query(StatisticEntity).filter(StatisticEntity.id == statistic_id).first()
        if not statistic:
            return None

        update_fields = {k: v for k, v in updated_dto.dict().items() if k not in ["id", "user_id"] and v is not None}
        for key, value in update_fields.items():
            setattr(statistic, key, value)

        self.db.commit()
        self.db.refresh(statistic)

        return StatisticMapper.entity_to_dto(statistic)
