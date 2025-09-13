from persistence.entities.backtest_entity import BacktestEntity
from persistence.dto.backtest_dto import BacktestDTO

class BacktestMapper:
    @staticmethod
    def entity_to_dto(backtest: BacktestEntity) -> BacktestDTO:
        return BacktestDTO(
            id            = backtest.id,
            user_id       = backtest.user_id,
            strategy_id   = backtest.strategy_id,

            symbol        = backtest.symbol,
            time_frame    = backtest.time_frame,
            start_date    = backtest.start_date,
            end_date      = backtest.end_date,

            initial_balance = backtest.initial_balance,
            risk_per_trade  = backtest.risk_per_trade,

            total_profit    = backtest.total_profit,
            drawdown_max    = backtest.drawdown_max,
            winrate         = backtest.winrate,
            nr_trades       = backtest.nr_trades,
            profit_factor   = backtest.profit_factor,
            expectancy      = backtest.expectancy,
            balance_curve   = getattr(backtest, "balance_curve", None),

            created_at      = backtest.created_at,
            name            = backtest.name
        )

    @staticmethod
    def dto_to_entity(dto: BacktestDTO) -> BacktestEntity:
        return BacktestEntity(
            id            = dto.id,
            user_id       = dto.user_id,
            strategy_id   = dto.strategy_id,

            symbol        = dto.symbol,
            time_frame    = dto.time_frame,
            start_date    = dto.start_date,
            end_date      = dto.end_date,

            initial_balance = dto.initial_balance,
            risk_per_trade  = dto.risk_per_trade,

            total_profit    = dto.total_profit,
            drawdown_max    = dto.drawdown_max,
            winrate         = dto.winrate,
            nr_trades       = dto.nr_trades,
            profit_factor   = dto.profit_factor,
            expectancy      = dto.expectancy,
            balance_curve   = getattr(dto, "balance_curve", None),

            created_at      = dto.created_at,
            name            = dto.name
        )
