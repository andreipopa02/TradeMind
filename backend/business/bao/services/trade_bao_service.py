from datetime import time, datetime
from typing import List, Optional

from business.bto.trade_bto import TradeBTO
from business.mappers.trade_mapper import TradeMapper
from persistence.dal.trade_dal import TradeDAL
from business.bao.interfaces.trade_bao_interface import TradeBAOInterface
from persistence.entities.utils_entity import SourceType, SessionType, TradeType
from persistence.utils.data_validators import is_valid_time_and_date, is_valid_price, calculate_pips, \
    get_session_from_open_time, to_time


class TradeBAOService(TradeBAOInterface):
    def __init__(self, trade_dal: TradeDAL):
        self.dal = trade_dal

    def add_trade(self, trade_bto: TradeBTO) -> TradeBTO:
        is_valid_time_and_date(trade_bto)
        is_valid_price(trade_bto)
        trade_bto.pips = calculate_pips(trade_bto)

        trade_dto = TradeMapper.bto_to_dto(trade_bto)
        trade_dto.session = get_session_from_open_time(trade_bto)
        saved_trade_dto = self.dal.add_trade(trade_dto, trade_bto.user_id)
        return TradeMapper.dto_to_bto(saved_trade_dto)

    def delete_trade(self, trade_id: int) -> bool:
        return self.dal.delete_trade(trade_id)


    def get_trades_by_user(self, user_id: int) -> List[TradeBTO]:
        trade_dtos = self.dal.get_trades_by_source(user_id, source=SourceType.USER)
        return [TradeMapper.dto_to_bto(trade) for trade in trade_dtos]

    def get_trades_by_backtest(self, backtest_id: int) -> List[TradeBTO]:
        trade_dtos = self.dal.get_trades_by_backtest(backtest_id)
        return [TradeMapper.dto_to_bto(trade) for trade in trade_dtos]

    def get_trades_by_field(self, user_id: int, source: Optional[SourceType] = None, **filters) -> List[TradeBTO]:
        processed_filters = {}

        if "market" in filters:
            processed_filters["market"] = filters["market"]

        if "type" in filters:
            processed_filters["type"] = filters["type"]

        if "start_date" in filters and "end_date" in filters:
            processed_filters["open_date__range"] = (filters["start_date"], filters["end_date"])
        elif "start_date" in filters:
            processed_filters["open_date__gte"] = filters["start_date"]
        elif "end_date" in filters:
            processed_filters["open_date__lte"] = filters["end_date"]

        if "min_volume" in filters:
            processed_filters["volume__gte"] = filters["min_volume"]
        if "max_volume" in filters:
            processed_filters["volume__lte"] = filters["max_volume"]

        if "session" in filters:
            processed_filters["session"] = filters["session"]

        if "source_type" in filters:
            processed_filters["source_type"] = filters["source_type"]

        if "backtest_id" in filters:
            processed_filters["backtest_id"] = filters["backtest_id"]

        if filters.get("profit_filter"):
            if filters["profit_filter"] == "win":
                processed_filters["profit__gt"] = 0

            elif filters["profit_filter"] == "lose":
                processed_filters["profit__lt"] = 0

            elif filters["profit_filter"] == "be":
                processed_filters["profit"] = 0

        trade_dtos = self.dal.get_trades_by_field(user_id, source, **processed_filters)
        return [TradeMapper.dto_to_bto(trade) for trade in trade_dtos]


    def update_trade(self, trade_id: int, updated_trade_bto: TradeBTO) -> Optional[TradeBTO]:
        is_valid_time_and_date(updated_trade_bto)
        is_valid_price(updated_trade_bto)
        updated_trade_bto.pips = calculate_pips(updated_trade_bto)

        updated_trade_dto = TradeMapper.bto_to_dto(updated_trade_bto)
        updated_trade_dto.session = get_session_from_open_time(updated_trade_bto)

        result_dto = self.dal.update_trade(trade_id, updated_trade_dto)
        return TradeMapper.dto_to_bto(result_dto) if result_dto else None
