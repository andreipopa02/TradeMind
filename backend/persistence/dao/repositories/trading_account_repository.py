import hashlib
from sqlalchemy.orm import Session
from typing import List, Optional

from persistence.dao.interfaces.trading_account_dao_interface import TradingAccountDAOInterface
from persistence.dto.trading_account_dto import TradingAccountDTO
from persistence.entities.trading_account_entity import TradingAccountEntity
from persistence.mappers.trading_account_mapper import TradingAccountMapper
from persistence.utils.encryption import encrypt, decrypt


class TradingAccountRepository(TradingAccountDAOInterface):
    def __init__(self, db: Session):
        self.session = db


    # Create & Delete
    def register_trading_account(self, account_dto: TradingAccountDTO) -> TradingAccountDTO:
        try:
            dto = account_dto.copy()
            dto.password = encrypt(dto.password)
            new_account = TradingAccountMapper.dto_to_entity(dto)

            self.session.add(new_account)
            self.session.commit()
            self.session.refresh(new_account)

            return TradingAccountMapper.entity_to_dto(new_account)
        except():
            self.session.rollback()


    def delete_trading_account(self, account_id: int) -> None:
        account = self.get_account_by_id(account_id)
        if account:
            self.session.delete(account)
            self.session.commit()


    # Get all accounts
    def get_user_accounts(self, user_id: int) -> List[TradingAccountDTO]:
        accounts = self.session.query(TradingAccountEntity).filter_by(user_id=user_id).all()
        dtos = []
        for acc in accounts:
            dto = TradingAccountMapper.entity_to_dto(acc)
            dto.password = decrypt(dto.password)
            dtos.append(dto)
        return dtos

    # Getters
    def get_credentials_by_id(self, account_id: int) -> Optional[TradingAccountDTO]:
        account = self.session.query(TradingAccountEntity).filter_by(account_id=account_id).first()
        if account:
            dto = TradingAccountMapper.entity_to_dto(account)
            dto.password = decrypt(dto.password)
            return dto
        return None

    def get_accounts_by_broker(self, broker_name: str) -> List[TradingAccountDTO]:
        accounts = self.session.query(TradingAccountEntity).filter_by(broker_name=broker_name).all()
        dtos = []
        for acc in accounts:
            dto = TradingAccountMapper.entity_to_dto(acc)
            dtos.append(dto)
        return dtos