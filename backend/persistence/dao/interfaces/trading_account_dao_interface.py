from typing import List, Optional

from persistence.dto.trading_account_dto import TradingAccountDTO
from persistence.entities.trading_account_entity import TradingAccountEntity


class TradingAccountDAOInterface:

    # Create & delete
    def register_trading_account(self, account_dto: TradingAccountDTO) -> TradingAccountDTO:
        pass

    def delete_trading_account(self, account_id: int) -> None:
        pass

    # Get all accounts
    def get_user_accounts(self, user_email: int) -> List[TradingAccountDTO]:
        pass

    # Getters
    def get_account_by_id(self, account_id: int) -> Optional[TradingAccountEntity]:
        pass

    def get_accounts_by_broker(self, broker_name: str) -> List[TradingAccountDTO]:
        pass

    def get_credentials_by_id(self, account_id: int) -> TradingAccountDTO:
        pass