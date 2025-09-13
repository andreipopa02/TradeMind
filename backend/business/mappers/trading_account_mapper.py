from business.bto.trading_account_bto import TradingAccountBTO
from persistence.dto.trading_account_dto import TradingAccountDTO


class TradingAccountMapper:
    @staticmethod
    def dto_to_bto(trading_account_dto: TradingAccountDTO) -> TradingAccountBTO:
        return TradingAccountBTO(
            id          = trading_account_dto.id,
            user_id     = trading_account_dto.user_id,

            broker_name = trading_account_dto.broker_name,
            account_id  = trading_account_dto.account_id,
            server      = trading_account_dto.server,
            password    = trading_account_dto.password
        )

    @staticmethod
    def bto_to_dto(trading_account_bto: TradingAccountBTO) -> TradingAccountDTO:
        return TradingAccountDTO(
            id          = trading_account_bto.id,
            user_id     = trading_account_bto.user_id,

            broker_name = trading_account_bto.broker_name,
            account_id  = trading_account_bto.account_id,
            server      = trading_account_bto.server,
            password    = trading_account_bto.password,
        )