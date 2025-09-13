from business.bto.backtest_bto import BacktestBTO
from persistence.dto.backtest_dto import BacktestDTO


class BacktestMapper:
    @staticmethod
    def dto_to_bto(dto: BacktestDTO) -> BacktestBTO:
        return BacktestBTO(
            id            = dto.id,
            user_id       = dto.user_id,
            strategy_id   = dto.strategy_id,

            symbol        = dto.symbol,
            time_frame    = dto.time_frame,
            start_date    = dto.start_date,
            end_date      = dto.end_date,

            initial_balance = dto.initial_balance,
            risk_per_trade  = dto.risk_per_trade,

            total_profit  = dto.total_profit,
            drawdown_max  = dto.drawdown_max,
            winrate       = dto.winrate,
            nr_trades     = dto.nr_trades,
            profit_factor = dto.profit_factor,
            expectancy    = dto.expectancy,
            balance_curve = getattr(dto, "balance_curve", None),

            created_at    = dto.created_at,
            name          = dto.name
        )

    @staticmethod
    def bto_to_dto(bto: BacktestBTO) -> BacktestDTO:
        return BacktestDTO(
            id            = bto.id,
            user_id       = bto.user_id,
            strategy_id   = bto.strategy_id,

            symbol        = bto.symbol,
            time_frame    = bto.time_frame,
            start_date    = bto.start_date,
            end_date      = bto.end_date,

            initial_balance = bto.initial_balance,
            risk_per_trade  = bto.risk_per_trade,

            total_profit  = bto.total_profit,
            drawdown_max  = bto.drawdown_max,
            winrate       = bto.winrate,
            nr_trades     = bto.nr_trades,
            profit_factor = bto.profit_factor,
            expectancy    = bto.expectancy,
            balance_curve = getattr(bto, "balance_curve", None),
            created_at    = bto.created_at,
            name          = bto.name
        )
