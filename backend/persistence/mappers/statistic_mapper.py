from persistence.dto.statistic_dto import StatisticDTO
from persistence.entities.statistic_entity import StatisticEntity


class StatisticMapper:
    @staticmethod
    def entity_to_dto(statistic: StatisticEntity) -> StatisticDTO:
        return StatisticDTO(
            id          = statistic.id,
            user_id     = statistic.user_id,
            name        = statistic.name,
            params      = statistic.params,
            is_active   = statistic.is_active,
            created_at  = statistic.created_at,
            updated_at  = statistic.updated_at
        )

    @staticmethod
    def dto_to_entity(dto: StatisticDTO) -> StatisticEntity:
        return StatisticEntity(
            id          = dto.id,
            user_id     = dto.user_id,
            name        = dto.name,
            params      = dto.params,
            is_active   = dto.is_active,
            created_at  = dto.created_at,
            updated_at  = dto.updated_at
        )
