from typing import Dict, List

from presentation.pao.interfaces.trade_pao_interface import TradePAOInterface
from business.bal.trade_bal import TradeBAL
from business.bto.trade_bto import TradeBTO
from persistence.entities.utils_entity import SourceType


class TradePAOService(TradePAOInterface):
    def __init__(self, bal: TradeBAL):
        self.bal = bal

    def request_to_bto(self, trade_data: Dict) -> TradeBTO:
        if "user_id" not in trade_data or "market" not in trade_data or "open_price" not in trade_data:
            raise ValueError("Missing required fields!")

        return TradeBTO(
            id=None,
            user_id=trade_data["user_id"],

            market=trade_data["market"],
            volume=trade_data["volume"],
            type=trade_data["type"],

            open_date=trade_data["open_date"],
            open_time=trade_data["open_time"],
            close_date=trade_data.get("close_date"),
            close_time=trade_data.get("close_time"),
            session=trade_data.get("session"),

            open_price=trade_data["open_price"],
            close_price=trade_data.get("close_price"),
            sl_price=trade_data.get("sl_price"),
            tp_price=trade_data.get("tp_price"),

            swap=trade_data.get("swap"),
            commission=trade_data.get("commission"),
            profit=trade_data.get("profit"),
            pips=trade_data.get("pips"),

            link_photo=trade_data.get("link_photo"),

            source_type=trade_data.get("source_type", SourceType.UNKNOWN),
            backtest_id=trade_data.get("backtest_id"),
        )

    def bto_to_response(self, trade_bto: TradeBTO) -> Dict:
        return {
            "id": trade_bto.id,
            "user_id": trade_bto.user_id,

            "market": trade_bto.market,
            "volume": trade_bto.volume,
            "type": trade_bto.type,

            "open_date": trade_bto.open_date,
            "open_time": trade_bto.open_time,
            "close_date": trade_bto.close_date,
            "close_time": trade_bto.close_time,
            "session":  trade_bto.session,

            "open_price": trade_bto.open_price,
            "close_price": trade_bto.close_price,
            "sl_price": trade_bto.sl_price,
            "tp_price": trade_bto.tp_price,

            "swap": trade_bto.swap,
            "commission": trade_bto.commission,
            "profit": trade_bto.profit,
            "pips": trade_bto.pips,

            "link_photo": trade_bto.link_photo,

            "source_type": trade_bto.source_type,
            "backtest_id": trade_bto.backtest_id,
        }

    def add_trade(self, trade_data: dict) -> dict:
        trade_bto = self.request_to_bto(trade_data)
        created_trade = self.bal.add_trade(trade_bto)
        return self.bto_to_response(created_trade)

    def update_trade(self, trade_id: int, updated_trade_data: dict) -> dict:
        trade_bto = self.request_to_bto(updated_trade_data)
        updated_trade = self.bal.update_trade(trade_id, trade_bto)
        return self.bto_to_response(updated_trade) if updated_trade else None

    def delete_trade(self, trade_id: int) -> bool:
        return self.bal.delete_trade(trade_id)

    def get_trades_by_field(self, user_id: int, source: SourceType, filters: dict) -> List[dict]:
        trades_bto = self.bal.get_trades_by_field(user_id, source, **filters)
        return [self.bto_to_response(trade) for trade in trades_bto]

    def get_trades_by_user(self, user_id: int) -> List[dict]:
        trades_bto = self.bal.get_trades_by_user(user_id)
        return [self.bto_to_response(trade) for trade in trades_bto]

    def get_trades_by_backtest(self, backtest_id: int) -> List[dict]:
        trades_bto = self.bal.get_trades_by_backtest(backtest_id)
        return [self.bto_to_response(trade) for trade in trades_bto]
