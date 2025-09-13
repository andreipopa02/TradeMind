from persistence.dto.trading_account_dto import TradingAccountDTO
from persistence.entities.trading_account_entity import TradingAccountEntity


class TradingAccountMapper:
    @staticmethod
    def entity_to_dto(entity: TradingAccountEntity) -> TradingAccountDTO:
        return TradingAccountDTO(
            id          = entity.id,
            user_id     = entity.user_id,

            broker_name = entity.broker_name,
            account_id  = entity.account_id,
            server      = entity.server,
            password    = entity.password,
        )

    @staticmethod
    def dto_to_entity(dto: TradingAccountDTO) -> TradingAccountEntity:
        return TradingAccountEntity(
            id          = dto.id,
            user_id     = dto.user_id,

            broker_name = dto.broker_name,
            account_id  = dto.account_id,
            server      = dto.server,
            password    = dto.password,
        )