from typing import List

from business.bto.trading_account_bto import TradingAccountBTO
from presentation.pao.interfaces.trading_account_pao_interface import TradingAccountPAOInterface
from presentation.pao.services.trading_account_pao_service import TradingAccountPAOService


class TradingAccountPAL:
    def __init__(self, trading_account_pao: TradingAccountPAOService):
        self.trading_account_pao = trading_account_pao

    # Create & delete
    def register_trading_account(self, account_data: dict) -> dict:
        return self.trading_account_pao.register_trading_account(account_data)

    def delete_trading_account(self, account_id: int) -> None:
        return self.trading_account_pao.delete_trading_account(account_id)

    # Getters
    def get_account_info_by_id(self, account_id: int, force_reload: bool = False) -> dict:
        return self.trading_account_pao.get_account_info_by_id(account_id, force_reload)

    def get_trade_history_by_id(self, account_id: int) -> List[dict]:
        return self.trading_account_pao.get_trade_history_by_id(account_id)

    def get_active_trades_by_id(self, account_id: int) -> List[dict]:
        return self.trading_account_pao.get_active_trades_by_id(account_id)

    def get_account_performance(self, account_id: int) -> List[dict]:
        return self.trading_account_pao.get_account_performance(account_id)

    def get_account_stats(self, account_id: int) -> dict:
        return self.trading_account_pao.get_account_stats(account_id)

    def get_account_trading_journal(self, account_id: int) -> List[dict]:
        return self.trading_account_pao.get_account_trading_journal(account_id)


    def get_credentials_by_id(self, account_id: int) -> TradingAccountBTO:
        return self.trading_account_pao.get_credentials_by_id(account_id)

    def get_accounts_by_broker(self, broker_name: str) -> List[TradingAccountBTO]:
        return self.trading_account_pao.get_accounts_by_broker(broker_name)

    # Get all
    def get_trading_accounts(self, user_id: int) -> List[dict]:
        return self.trading_account_pao.get_trading_accounts(user_id)