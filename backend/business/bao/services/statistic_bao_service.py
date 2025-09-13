from collections import defaultdict
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from business.bao.interfaces.statistic_bao_interface import StatisticBAOInterface
from business.bao.services.trade_bao_service import TradeBAOService
from business.bto.statistic_bto import StatisticBTO
from business.bto.trade_bto import TradeBTO
from business.mappers.statistic_mapper import StatisticMapper
from persistence.dal.statistic_dal import StatisticDAL
from persistence.dal.trade_dal import TradeDAL
from persistence.entities.utils_entity import SessionType, TradeType
from persistence.utils.data_validators import validate_statistic_params, validate_statistic_name


def parse_statistic_params(params: Dict[str, Any]) -> Dict[str, Any]:
    filters = {}

    if "market" in params:
        filters["market"] = params["market"]  # list -> handled in DAL

    if "session" in params:
        try:
            filters["session__in"] = [SessionType(s) for s in params["session"]]
        except ValueError as e:
            raise ValueError(f"Invalid session type: {e}")

    if "source_type" in params:
        filters["source_type"] = params["source_type"].upper()

    if "min_volume" in params:
        filters["min_volume"] = float(params["min_volume"])

    if "max_volume" in params:
        filters["max_volume"] = float(params["max_volume"])

    if "start_date" in params:
        filters["start_date"] = datetime.strptime(params["start_date"], "%Y-%m-%d").date()

    if "end_date" in params:
        filters["end_date"] = datetime.strptime(params["end_date"], "%Y-%m-%d").date()

    if "backtest_id" in params:
        try:
            filters["backtest_id"] = int(params["backtest_id"])
        except ValueError:
            raise ValueError(f"Invalid backtest_id: {params['backtest_id']}")

    return filters


class StatisticBAOService(StatisticBAOInterface):
    def __init__(self, db: Session, statistic_dal: StatisticDAL):
        self.dal = statistic_dal

        trade_dal = TradeDAL(db)
        self.trade_service = TradeBAOService(trade_dal)


    def create_statistic(self, bto: StatisticBTO) -> StatisticBTO:
        validate_statistic_name(bto.name)
        validate_statistic_params(bto.params)

        dto = StatisticMapper.bto_to_dto(bto)
        saved_dto = self.dal.add_statistic(dto, user_id=bto.user_id)
        return StatisticMapper.dto_to_bto(saved_dto)

    def delete_statistic(self, statistic_id: int) -> bool:
        return self.dal.delete_statistic(statistic_id)


    # Getters
    def get_statistic_by_id(self, statistic_id: int) -> Optional[StatisticBTO]:
        dto = self.dal.get_statistic_by_id(statistic_id)
        return StatisticMapper.dto_to_bto(dto) if dto else None

    def get_statistics_by_user(self, user_id: int) -> List[StatisticBTO]:
        dtos = self.dal.get_statistics_by_user(user_id)
        return [StatisticMapper.dto_to_bto(dto) for dto in dtos]


    # Setters
    def update_statistic(self, statistic_id: int, updated_bto: StatisticBTO) -> Optional[StatisticBTO]:
        updated_dto = StatisticMapper.bto_to_dto(updated_bto)
        result_dto = self.dal.update_statistic(statistic_id, updated_dto)
        return StatisticMapper.dto_to_bto(result_dto) if result_dto else None


    # Others
    def generate_statistics(self, bto: StatisticBTO) -> dict:
        params = bto.params or {}
        filters = parse_statistic_params(params)

        trades = self.trade_service.get_trades_by_field(bto.user_id, **filters)

        result = self._calculate_metrics(trades, bto.name, filters)
        return result

    def _calculate_metrics(self, trades: List[TradeBTO], name: str, filters: dict) -> dict:
        total = len(trades)
        if total == 0:
            return {
                "statistic_name": name,
                "filters_applied": filters,
                "metrics": {
                    "total_trades": 0,
                    "winrate": 0,
                    "lossrate": 0,
                    "break_even": 0,
                    "avg_rr": None,
                    "avg_profit": None,
                    "avg_loss": None,
                    "total_result": 0,
                    "max_profit": None,
                    "max_loss": None,
                    "balance_curve": [],
                    "long_stats": {},
                    "short_stats": {},
                    "by_instrument": [],
                    "by_day": [],
                    "by_duration": []
                }
            }

        wins = [t for t in trades if t.profit and t.profit > 0]
        losses = [t for t in trades if t.profit and t.profit < 0]
        be = [t for t in trades if t.profit == 0]

        rr_list = []
        for t in trades:
            if t.tp_price and t.sl_price and t.open_price:
                rr = abs(t.tp_price - t.open_price) / abs(
                    t.open_price - t.sl_price) if t.sl_price != t.open_price else None
                if rr:
                    rr_list.append(rr)

        profits = [t.profit for t in trades if t.profit is not None]

        balance_curve = []
        cumulative_balance = 0
        for idx, t in enumerate(trades):
            profit = t.profit if t.profit is not None else 0
            cumulative_balance += profit
            balance_curve.append({
                "trade": idx + 1,
                "balance": round(cumulative_balance, 2)
            })

        # Long vs Short
        long_trades = [t for t in trades if t.type == TradeType.BUY]
        short_trades = [t for t in trades if t.type == TradeType.SELL]

        def stat_info(trades_subset):
            if not trades_subset:
                return {"count": 0, "profit": 0.0, "winrate": 0}
            total_profit = sum(t.profit for t in trades_subset if t.profit is not None)
            wins = [t for t in trades_subset if t.profit and t.profit > 0]
            return {
                "count": len(trades_subset),
                "profit": round(total_profit, 2),
                "winrate": round(len(wins) / len(trades_subset) * 100, 2)
            }



        instrument_map = defaultdict(list)
        for t in trades:
            instrument_map[t.market].append(t)

        by_instrument = []
        for market, market_trades in instrument_map.items():
            profit = sum(t.profit for t in market_trades if t.profit is not None)
            by_instrument.append({
                "instrument": market,
                "trades": len(market_trades),
                "profit": round(profit, 2)
            })

        # By day of week
        day_map = defaultdict(list)
        for t in trades:
            if t.open_date:
                dt = datetime.combine(t.open_date, datetime.min.time())
                day = dt.strftime('%A')
                day_map[day].append(t)

        by_day = []
        for day, day_trades in day_map.items():
            profit = sum(t.profit for t in day_trades if t.profit is not None)
            by_day.append({
                "day": day,
                "trades": len(day_trades),
                "profit": round(profit, 2)
            })

        # By duration
        duration_bins = {
            '0-1h': [],
            '1-4h': [],
            '4-12h': [],
            '12-24h': [],
            '>24h': []
        }

        for t in trades:
            if t.open_date and t.open_time and t.close_date and t.close_time:
                open_dt = datetime.combine(t.open_date, t.open_time)
                close_dt = datetime.combine(t.close_date, t.close_time)
                duration = (close_dt - open_dt).total_seconds() / 3600
                if duration <= 1:
                    duration_bins['0-1h'].append(t)
                elif duration <= 4:
                    duration_bins['1-4h'].append(t)
                elif duration <= 12:
                    duration_bins['4-12h'].append(t)
                elif duration <= 24:
                    duration_bins['12-24h'].append(t)
                else:
                    duration_bins['>24h'].append(t)

        by_duration = []
        for label, group in duration_bins.items():
            profit = sum(t.profit for t in group if t.profit is not None)
            by_duration.append({
                "range": label,
                "trades": len(group),
                "profit": round(profit, 2)
            })

        return {
            "statistic_name": name,
            "filters_applied": filters,
            "metrics": {
                "total_trades": total,
                "winrate": round(len(wins) / total * 100, 2),
                "lossrate": round(len(losses) / total * 100, 2),
                "break_even": len(be),
                "avg_rr": round(sum(rr_list) / len(rr_list), 2) if rr_list else None,
                "avg_profit": round(sum(t.profit for t in wins) / len(wins), 2) if wins else None,
                "avg_loss": round(sum(t.profit for t in losses) / len(losses), 2) if losses else None,
                "total_result": round(sum(profits), 2),
                "max_profit": max(profits, default=None),
                "max_loss": min(profits, default=None),
                "balance_curve": balance_curve,
                "long_stats": stat_info(long_trades),
                "short_stats": stat_info(short_trades),
                "by_instrument": by_instrument,
                "by_day": by_day,
                "by_duration": by_duration
            }
        }
