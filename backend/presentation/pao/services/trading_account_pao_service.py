from typing import Dict, List

from presentation.pao.interfaces.trading_account_pao_interface import TradingAccountPAOInterface
from business.bal.trading_account_bal import TradingAccountBAL
from business.bto.trading_account_bto import TradingAccountBTO


class TradingAccountPAOService(TradingAccountPAOInterface):
    def __init__(self, bal: TradingAccountBAL):
        self.bal = bal

    def request_to_bto(self, account_data: Dict) -> TradingAccountBTO:
        if ("user_id" not in account_data
                or "broker_name" not in account_data
                or "account_id" not in account_data
                or "server" not in account_data
                or "password" not in account_data):
            raise ValueError("Missing required fields!")
        return TradingAccountBTO(
            id=None,
            user_id=account_data["user_id"],

            broker_name=account_data["broker_name"],
            account_id=account_data.get("account_id", ""),
            server=account_data.get("server", ""),
            password=account_data.get("password", "")
        )

    def bto_to_response(self, account_bto: TradingAccountBTO) -> Dict:
        return {
            "id": account_bto.id,
            "user_id": account_bto.user_id,

            "broker_name": account_bto.broker_name,
            "account_id": account_bto.account_id,
            "server": account_bto.server,
            "password": account_bto.password,

            "balance": account_bto.balance,
            "equity": account_bto.equity,
        }

    # Create & delete
    def register_trading_account(self, account_data: dict)  -> dict:
        account_bto = self.request_to_bto(account_data)
        created_account = self.bal.register_trading_account(account_bto)
        return self.bto_to_response(created_account)

    def delete_trading_account(self, account_id: int) -> None:
        return self.bal.delete_trading_account(account_id)

    # Getters
    def get_account_info_by_id(self, account_id: int, force_reload: bool = False) -> dict:
        return self.bal.get_account_info_by_id(account_id, force_reload)

    def get_trade_history_by_id(self, account_id: int) -> List[dict]:
        return self.bal.get_trade_history_by_id(account_id)

    def get_active_trades_by_id(self, account_id: int) -> List[dict]:
        return self.bal.get_active_trades_by_id(account_id)

    def get_account_performance(self, account_id: int) -> List[dict]:
        return self.bal.get_account_performance(account_id)

    def get_account_stats(self, account_id: int) -> dict:
        return self.bal.get_account_stats(account_id)

    def get_account_trading_journal(self, account_id: int) -> List[dict]:
        return self.bal.get_account_trading_journal(account_id)

    def get_credentials_by_id(self, account_id: int) -> TradingAccountBTO:
        return self.bal.get_credentials_by_id(account_id)

    def get_accounts_by_broker(self, broker_name: str) -> List[TradingAccountBTO]:
        return self.bal.get_accounts_by_broker(broker_name)

    # Get all
    def get_trading_accounts(self, user_id: int) -> List[dict]:
        accounts_bto = self.bal.get_trading_accounts(user_id)
        return [self.bto_to_response(account) for account in accounts_bto]
