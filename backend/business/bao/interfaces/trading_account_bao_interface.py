from business.bto.trading_account_bto import TradingAccountBTO
from typing import List, Optional


class TradingAccountBAOInterface:

    # Create & Delete
    def register_trading_account(self, account_bto: TradingAccountBTO) -> TradingAccountBTO:
        pass

    def delete_trading_account(self, account_id: int) -> None:
        pass

    # Getters
    def get_account_info_by_id(self, account_id: int, force_reload: bool = False) -> dict:
        pass

    def get_active_trades_by_id(self, account_id: int) -> List[dict]:
        pass

    def get_trade_history_by_id(self, account_id: int) -> List[dict]:
        pass

    def get_credentials_by_id(self, account_id: int) -> Optional[TradingAccountBTO]:
        pass

    def get_account_performance(self, account_id: int) -> List[dict]:
        pass

    def get_account_stats(self, account_id: int) -> dict:
        pass

    def get_account_trading_journal(self, account_id: int) -> List[dict]:
        pass

    def get_accounts_by_broker(self, broker_name: str) -> List[TradingAccountBTO]:
        pass

    # Get all accounts
    def get_user_accounts(self, user_id: int) -> List[TradingAccountBTO]:
        pass