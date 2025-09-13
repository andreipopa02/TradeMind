from typing import Type
from business.utils.strategies.base_strategy import BaseStrategy
from persistence.entities.utils_entity import StrategyType

from business.utils.strategies.ema_crossover_strategy import EMACrossoverStrategy
from business.utils.strategies.sma_crossover_strategy import SMACrossoverStrategy
from business.utils.strategies.rsi_strategy_strategy import RSIStrategy
from business.utils.strategies.bollinger_bands_strategy import BollingerBandsStrategy
from business.utils.strategies.breakout_strategy import BreakoutStrategy
from business.utils.strategies.donchian_channel_strategy import DonchianChannelStrategy
from business.utils.strategies.engulfing_strategy import EngulfingPatternStrategy
from business.utils.strategies.hammer_shooting_star_strategy import HammerShootingStarStrategy
from business.utils.strategies.head_and_shoulders_strategy import HeadAndShouldersStrategy
from business.utils.strategies.double_top_bottom_strategy import DoubleTopBottomStrategy
from business.utils.strategies.inside_bar_strategy import InsideBarStrategy


class StrategyRegistry:
    _registry: dict[StrategyType, Type[BaseStrategy]] = {
        StrategyType.EMA_CROSSOVER: EMACrossoverStrategy,
        StrategyType.SMA_CROSSOVER: SMACrossoverStrategy,
        StrategyType.RSI_OVERBOUGHT_OVERSOLD: RSIStrategy,
        StrategyType.BOLLINGER_BANDS: BollingerBandsStrategy,
        StrategyType.BREAKOUT: BreakoutStrategy,
        StrategyType.DONCHIAN_CHANNEL: DonchianChannelStrategy,
        StrategyType.ENGULFING_PATTERN: EngulfingPatternStrategy,
        StrategyType.HAMMER_SHOOTING_STAR: HammerShootingStarStrategy,
        StrategyType.HEAD_AND_SHOULDERS: HeadAndShouldersStrategy,
        StrategyType.DOUBLE_TOP_BOTTOM: DoubleTopBottomStrategy,
        StrategyType.INSIDE_BAR: InsideBarStrategy,
    }

    @classmethod
    def get_strategy(cls, strategy_type: StrategyType) -> BaseStrategy:
        strategy_class = cls._registry.get(strategy_type)
        if not strategy_class:
            raise ValueError(f"Strategy type '{strategy_type}' is not implemented.")
        return strategy_class()
