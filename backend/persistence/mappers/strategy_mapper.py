from persistence.entities.strategy_entity import StrategyEntity
from persistence.dto.strategy_dto import StrategyDTO

class StrategyMapper:
    @staticmethod
    def entity_to_dto(strategy: StrategyEntity) -> StrategyDTO:
        return StrategyDTO(
            id          = strategy.id,
            name        = strategy.name,
            description = strategy.description,
            type        = strategy.type,
            parameters  = strategy.parameters,
            created_by  = strategy.created_by,
            is_public   = strategy.is_public,
            created_at  = strategy.created_at
        )

    @staticmethod
    def dto_to_entity(dto: StrategyDTO) -> StrategyEntity:
        return StrategyEntity(
            id          = dto.id,
            name        = dto.name,
            description = dto.description,
            type        = dto.type,
            parameters  = dto.parameters,
            created_by  = dto.created_by,
            is_public   = dto.is_public,
            created_at  = dto.created_at
        )
