from business.bao.services.trading_account_bao_service import TradingAccountBAOService
from business.bto.trading_account_bto import TradingAccountBTO
from typing import List, Optional


class TradingAccountBAL:
    def __init__(self, trading_account_bao: TradingAccountBAOService):
        self.trading_account_bao = trading_account_bao

    # Create & delete
    def register_trading_account(self, account_bto) -> TradingAccountBTO:
        return self.trading_account_bao.register_trading_account(account_bto)

    def delete_trading_account(self, account_id: int) -> None:
        self.trading_account_bao.delete_trading_account(account_id)

    # Getters
    def get_account_info_by_id(self, account_id: int, force_reload: bool = False) -> dict:
        return self.trading_account_bao.get_account_info_by_id(account_id, force_reload)

    def get_active_trades_by_id(self, account_id: int)-> List[dict]:
        return self.trading_account_bao.get_active_trades_by_id(account_id)

    def get_trade_history_by_id(self, account_id: int) -> List[dict]:
        return self.trading_account_bao.get_trade_history_by_id(account_id)

    def get_account_performance(self, account_id: int) -> List[dict]:
        return self.trading_account_bao.get_account_performance(account_id)

    def get_account_stats(self, account_id: int) -> dict:
        return self.trading_account_bao.get_account_stats(account_id)

    def get_account_trading_journal(self, account_id: int) -> List[dict]:
        return self.trading_account_bao.get_account_trading_journal(account_id)

    def get_credentials_by_id(self, account_id: int) -> Optional[TradingAccountBTO]:
        return self.trading_account_bao.get_credentials_by_id(account_id)

    def get_accounts_by_broker(self, broker_name: str) -> List[TradingAccountBTO]:
        return self.trading_account_bao.get_accounts_by_broker(broker_name)

    # Get all
    def get_trading_accounts(self, user_id: int) -> List[TradingAccountBTO]:
        return self.trading_account_bao.get_user_accounts(user_id)