from business.bto.strategy_bto import StrategyBTO
from persistence.dto.strategy_dto import StrategyDTO

class StrategyMapper:
    @staticmethod
    def dto_to_bto(dto: StrategyDTO) -> StrategyBTO:
        return StrategyBTO(
            id          = dto.id,
            name        = dto.name,
            type        = dto.type,
            description = dto.description,
            parameters  = dto.parameters,
            is_public   = dto.is_public,
            created_by  = dto.created_by,
            created_at  = dto.created_at
        )

    @staticmethod
    def bto_to_dto(bto: StrategyBTO) -> StrategyDTO:
        return StrategyDTO(
            id          = bto.id,
            name        = bto.name,
            type        = bto.type,
            description = bto.description,
            parameters  = bto.parameters,
            is_public   = bto.is_public,
            created_by  = bto.created_by,
            created_at  = bto.created_at
        )
