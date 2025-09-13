from typing import Dict, List

from business.bto.trade_bto import TradeBTO
from persistence.entities.utils_entity import SourceType


class TradePAOInterface:
    def request_to_bto(self, trade_data: Dict) -> TradeBTO:
        pass

    def bto_to_response(self, trade_bto: TradeBTO) -> Dict:
        pass

    def add_trade(self, trade_data: dict) -> dict:
        pass

    def update_trade(self, trade_id: int, updated_trade_data: dict) -> dict:
        pass

    def delete_trade(self, trade_id: int) -> bool:
        pass

    def get_trades_by_field(self, user_id: int, source: SourceType, filters: dict) -> List[dict]:
        pass

    def get_trades_by_user(self, user_id: int) -> List[dict]:
        pass

    def get_trades_by_backtest(self, backtest_id: int) -> List[dict]:
        pass
