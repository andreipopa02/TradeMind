from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException
from cachetools import TTLCache

from mt5_service.mt5_client import get_account_info, get_active_trades, get_trade_history, check_credentials

from business.bao.interfaces.trading_account_bao_interface import TradingAccountBAOInterface
from business.mappers.trading_account_mapper import TradingAccountMapper
from mt5_service.mt5_client import get_account_performance, get_account_stats, get_account_trading_journal
from persistence.dal.trading_account_dal import TradingAccountDAL
from business.bto.trading_account_bto import TradingAccountBTO


class TradingAccountBAOService(TradingAccountBAOInterface):
    def __init__(self, trading_account_dal: TradingAccountDAL):
        self.account_info_cache = TTLCache(maxsize=100, ttl=600)
        self.trading_account_dal = trading_account_dal


    # Create & delete
    def register_trading_account(self, account_bto: TradingAccountBTO) -> TradingAccountBTO:
        existing_account = self.trading_account_dal.get_account_by_id(account_bto.account_id)
        if existing_account:
            raise HTTPException(status_code=400, detail="An account with this ID already exists in out database.")

        credentials_valid = check_credentials(
            account_id=account_bto.account_id,
            password=account_bto.password,
            server=account_bto.server
        )

        if "error" in credentials_valid:
            raise HTTPException(status_code=401, detail="Invalid trading account credentials. Registration failed.")

        account_dto = TradingAccountMapper.bto_to_dto(account_bto)

        try:
            new_account = self.trading_account_dal.register_trading_account(account_dto)

            account_info = get_account_info(account_bto.account_id, account_bto.password, account_bto.server)
            if isinstance(account_info, dict):
                self.account_info_cache[account_bto.account_id] = account_info

            return TradingAccountMapper.dto_to_bto(new_account)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Account ID must be unique.")

    def delete_trading_account(self, account_id: int) -> None:
        return self.trading_account_dal.delete_trading_account(account_id)

    # Getters
    def get_account_info_by_id(self, account_id: int, force_reload: bool = False) -> dict:
        if not force_reload and account_id in self.account_info_cache:
            return self.account_info_cache[account_id]

        account_bto = self.get_credentials_by_id(account_id)
        account_info = get_account_info(account_bto.account_id, account_bto.password, account_bto.server)

        if not isinstance(account_info, dict):
            return {}

        self.account_info_cache[account_id] = account_info
        return account_info

    def get_active_trades_by_id(self, account_id: int) -> List[dict]:
        account_bto = self.trading_account_dal.get_credentials_by_id(account_id)
        account_trades = get_active_trades(account_bto.account_id, account_bto.password, account_bto.server)
        return account_trades

    def get_trade_history_by_id(self, account_id: int) -> List[dict]:
        account_bto = self.trading_account_dal.get_credentials_by_id(account_id)
        account_trades = get_trade_history(account_bto.account_id, account_bto.password, account_bto.server)
        return account_trades

    def get_account_performance(self, account_id: int) -> List[dict]:
        account_bto = self.get_credentials_by_id(account_id)
        performance_data = get_account_performance(account_bto.account_id, account_bto.password, account_bto.server)
        if not isinstance(performance_data, list):
            return []
        return performance_data

    def get_account_stats(self, account_id: int) -> dict:
        account_bto = self.get_credentials_by_id(account_id)
        stats_data = get_account_stats(account_bto.account_id, account_bto.password, account_bto.server)
        if not isinstance(stats_data, dict):
            return {}
        return stats_data

    def get_account_trading_journal(self, account_id: int) -> List[dict]:
        account_bto = self.get_credentials_by_id(account_id)
        trade_journal = get_account_trading_journal(account_bto.account_id, account_bto.password, account_bto.server)
        if not isinstance(trade_journal, list):
            return []
        return trade_journal

    def get_credentials_by_id(self, account_id: int) -> Optional[TradingAccountBTO]:
        return self.trading_account_dal.get_credentials_by_id(account_id)

    def get_accounts_by_broker(self, broker_name: str) -> List[TradingAccountBTO]:
        accounts = self.trading_account_dal.get_accounts_by_broker(broker_name)
        return [TradingAccountMapper.dto_to_bto(account) for account in accounts] if accounts else []

    # Get all
    def get_user_accounts(self, user_id: int) -> List[TradingAccountBTO]:
        accounts = self.trading_account_dal.get_user_accounts(user_id)

        if not accounts:
            raise HTTPException(status_code=404, detail="No trading accounts found for this user.")

        return [TradingAccountMapper.dto_to_bto(account) for account in accounts]
