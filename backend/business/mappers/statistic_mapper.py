from business.bto.statistic_bto import StatisticBTO
from persistence.dto.statistic_dto import StatisticDTO


class StatisticMapper:
    @staticmethod
    def dto_to_bto(dto: StatisticDTO) -> StatisticBTO:
        return StatisticBTO(
            id          = dto.id,
            user_id     = dto.user_id,

            name        = dto.name,
            params      = dto.params,
            is_active   = dto.is_active,

            created_at  = dto.created_at,
            updated_at  = dto.updated_at
        )

    @staticmethod
    def bto_to_dto(bto: StatisticBTO) -> StatisticDTO:
        return StatisticDTO(
            id          = bto.id,
            user_id     = bto.user_id,

            name        = bto.name,
            params      = bto.params,
            is_active   = bto.is_active,

            created_at  = bto.created_at,
            updated_at  = bto.updated_at
        )
