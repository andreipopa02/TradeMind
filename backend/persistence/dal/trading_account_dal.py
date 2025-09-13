from typing import Optional, List

from sqlalchemy.orm import Session

from persistence.dao.repositories.trading_account_repository import TradingAccountRepository
from persistence.dto.trading_account_dto import TradingAccountDTO
from persistence.entities.trading_account_entity import TradingAccountEntity


class TradingAccountDAL:
    def __init__(self, db: Session):
        self.repo = TradingAccountRepository(db)

    # Create & delete
    def register_trading_account(self, account_dto: TradingAccountDTO) -> TradingAccountDTO:
        return self.repo.register_trading_account(account_dto)

    def delete_trading_account(self, account_id: int) -> None:
        self.repo.delete_trading_account(account_id)

    # Get all accounts
    def get_user_accounts(self, user_id: int) -> List[TradingAccountDTO]:
        return self.repo.get_user_accounts(user_id)

    # Getters
    def get_account_by_id(self, account_id: int) -> Optional[TradingAccountEntity]:
        return self.repo.get_account_by_id(account_id)

    def get_credentials_by_id(self, account_id: int) -> Optional[TradingAccountDTO]:
        return self.repo.get_credentials_by_id(account_id)

    def get_accounts_by_broker(self, broker_name: str) -> List[TradingAccountDTO]:
        return self.repo.get_accounts_by_broker(broker_name)