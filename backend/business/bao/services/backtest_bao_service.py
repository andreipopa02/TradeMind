from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from business.bao.interfaces.backtest_bao_interface import BacktestBAOInterface
from business.bao.services.trade_bao_service import TradeBAOService
from business.bto.backtest_bto import BacktestBTO
from business.bto.trade_bto import TradeBTO
from business.mappers.backtest_mapper import BacktestMapper
from persistence.dal.backtest_dal import BacktestDAL
from business.utils.backtest.backtest_executor import BacktestExecutor
from business.utils.strategies.strategy_registry import StrategyRegistry
from business.bao.services.chart_data_bao_service import ChartDataBAOService
from business.bao.services.strategy_bao_service import StrategyBAOService
from persistence.dal.strategy_dal import StrategyDAL
from persistence.dal.trade_dal import TradeDAL
from persistence.entities.utils_entity import SourceType, SessionType
from business.utils.backtest.backtest_executor import map_action_to_trade_type

class BacktestBAOService(BacktestBAOInterface):
    def __init__(self, db: Session, backtest_dal: BacktestDAL):
        self.db = db
        self.dal = backtest_dal


    def save_backtest(self, bto: BacktestBTO, executed_trades: List[dict]) -> BacktestBTO:
        strategy_dal = StrategyDAL(self.db)
        strategy_bao = StrategyBAOService(self.db, strategy_dal)
        strategy_bto = strategy_bao.get_strategy_by_id(bto.strategy_id)

        # Generate backtest name
        bto.name = f"{strategy_bto.name}_${bto.initial_balance}_{bto.risk_per_trade}%_{bto.risk_reward_ratio}_{bto.start_date}_{bto.end_date}"
        bto.created_at = datetime.utcnow()

        # Save backtest
        dto = BacktestMapper.bto_to_dto(bto)
        saved_dto = self.dal.add_backtest(dto, user_id=bto.user_id)
        saved_backtest = BacktestMapper.dto_to_bto(saved_dto)

        # Save executed trades
        trade_dal = TradeDAL(self.db)
        trade_bao = TradeBAOService(trade_dal)

        for t in executed_trades:
            try:
                trade_bto = TradeBTO(
                    id=None,
                    user_id=bto.user_id,
                    backtest_id=saved_backtest.id,
                    market=bto.symbol,
                    volume=1,
                    type=map_action_to_trade_type(t["entry_action"]),
                    open_date=datetime.fromtimestamp(t["open_timestamp"]).date(),
                    open_time=datetime.fromtimestamp(t["open_timestamp"]).time(),
                    close_date=datetime.fromtimestamp(t["close_timestamp"]).date(),
                    close_time=datetime.fromtimestamp(t["close_timestamp"]).time(),
                    session=SessionType.UNKNOWN,
                    open_price=t["entry_price"],
                    close_price=t["exit_price"],
                    sl_price=t["sl_price"],
                    tp_price=t["tp_price"],
                    swap=0,
                    commission=0,
                    profit=t["profit"],
                    pips=t["pips"],
                    link_photo=None,
                    source_type=SourceType.BACKTEST
                )
                trade_bao.add_trade(trade_bto)
            except Exception as e:
                print("ERROR inserting trade:", t, str(e))
                raise

        return saved_backtest

    def run_backtest_preview(self, bto: BacktestBTO) -> dict:
        # Load candle data
        chart_bao = ChartDataBAOService()
        chart_data = chart_bao.get_chart_data({
            "symbol": bto.symbol,
            "time_frame": bto.time_frame,
            "start_date": bto.start_date.strftime("%Y-%m-%d") if isinstance(bto.start_date,
                                                                            datetime) else bto.start_date,
            "end_date": bto.end_date.strftime("%Y-%m-%d") if isinstance(bto.end_date, datetime) else bto.end_date
        })
        candles = chart_data.get("candles", [])

        #Load strategy
        strategy_dal = StrategyDAL(self.db)
        strategy_bao = StrategyBAOService(self.db, strategy_dal)
        strategy_bto = strategy_bao.get_strategy_by_id(int(bto.strategy_id))
        strategy = StrategyRegistry.get_strategy(strategy_bto.type)

        # Apply strategy
        signals = strategy.generate_trades(candles, strategy_bto.parameters or {})

        # Run executor
        executor = BacktestExecutor(
            initial_balance=bto.initial_balance,
            risk_per_trade=bto.risk_per_trade,
            risk_reward_ratio=bto.risk_reward_ratio
        )
        result = executor.simulate_trades(signals, candles, bto.time_frame, bto.symbol)

        executed_trades = result["executed_trades"]
        metrics = result["metrics"]
        return {
            "executed_trades": executed_trades,
            "metrics": metrics
        }

    def delete_backtest(self, backtest_id: int) -> bool:
        return self.dal.delete_backtest(backtest_id)

    def get_backtest_by_id(self, backtest_id: int) -> Optional[BacktestBTO]:
        dto = self.dal.get_backtest_by_id(backtest_id)
        return BacktestMapper.dto_to_bto(dto) if dto else None

    def get_backtests_by_user(self, user_id: int) -> List[BacktestBTO]:
        dtos = self.dal.get_backtests_by_user(user_id)
        return [BacktestMapper.dto_to_bto(dto) for dto in dtos]

    def get_backtests_by_strategy(self, strategy_id: int) -> List[BacktestBTO]:
        dtos = self.dal.get_backtests_by_strategy(strategy_id)
        return [BacktestMapper.dto_to_bto(dto) for dto in dtos]

    def get_backtest_metrics(self, backtest_id: int) -> Optional[dict]:
        return self.dal.get_backtest_metrics(backtest_id)

    def update_backtest(self, backtest_id: int, updated_bto: BacktestBTO) -> Optional[BacktestBTO]:
        updated_dto = BacktestMapper.bto_to_dto(updated_bto)
        result_dto = self.dal.update_backtest(backtest_id, updated_dto)
        return BacktestMapper.dto_to_bto(result_dto) if result_dto else None

    def update_backtest_metrics(self, backtest_id: int, metrics: dict) -> bool:
        return self.dal.update_backtest_metrics(backtest_id, metrics)
