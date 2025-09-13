from persistence.dto.user_dto import UserDTO
from persistence.entities.user_entity import UserEntity

from persistence.mappers.trading_account_mapper import TradingAccountMapper
# from persistence.mappers.backtest_mapper import BacktestMapper
# from persistence.mappers.event_mapper import EventMapper


class UserMapper:
    @staticmethod
    def entity_to_dto(user_entity: UserEntity) -> UserDTO:
        return UserDTO(
            id          = user_entity.id,
            first_name  = user_entity.first_name,
            last_name   = user_entity.last_name,
            email       = user_entity.email,
            password    = user_entity.password,
            phone       = user_entity.phone,
            gender      = user_entity.gender,
            country     = user_entity.country,
            is_verified = user_entity.is_verified,

            # trading_accounts = [TradingAccountMapper.entity_to_dto(acc) for acc in user_entity.trading_accounts]
            # backtests        = [BacktestMapper.entity_to_dto(bt) for bt in user_entity.backtests],
            # events           = [EventMapper.entity_to_dto(ev) for ev in user_entity.events]
        )

    @staticmethod
    def dto_to_entity(user_dto: UserDTO, hashed_password: str) -> UserEntity:
        user_entity = UserEntity(
            id          = user_dto.id,
            first_name  = user_dto.first_name,
            last_name   = user_dto.last_name,
            email       = user_dto.email,
            password    = hashed_password,
            phone       = user_dto.phone,
            gender      = user_dto.gender,
            country     = user_dto.country,
            is_verified = user_dto.is_verified
        )

        # if user_dto.trading_accounts:
        #     user_entity.trading_accounts = [TradingAccountMapper.dto_to_entity(acc) for acc in
        #                                     user_dto.trading_accounts]

        # if user_dto.backtests:
        #     user_entity.backtests        = [BacktestMapper.dto_to_entity(bt) for bt in user_dto.backtests]

        # if user_dto.events:
        #     user_entity.events           = [EventMapper.dto_to_entity(ev) for ev in user_dto.events]

        return user_entity