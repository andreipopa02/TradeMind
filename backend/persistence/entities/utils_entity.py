from enum import Enum as PyEnum

class TradeType(PyEnum):
    BUY      = "buy"
    SELL     = "sell"
    UNKNOWN = "unknown"

class SourceType(PyEnum):
    USER     = "user"
    BACKTEST = "backtest"
    UNKNOWN = "unknown"

class SessionType(PyEnum):
    ASIA     = "Asia"
    LONDON   = "London"
    NEW_YORK = "NewYork"
    UNKNOWN = "Unknown"

class StrategyType(PyEnum):
    ENGULFING_PATTERN       = "ENGULFING_PATTERN"
    HAMMER_SHOOTING_STAR    = "HAMMER_SHOOTING_STAR"
    HEAD_AND_SHOULDERS      = "HEAD_AND_SHOULDERS"
    DOUBLE_TOP_BOTTOM       = "DOUBLE_TOP_BOTTOM"
    INSIDE_BAR              = "INSIDE_BAR"

    SMA_CROSSOVER           = "SMA_CROSSOVER"
    EMA_CROSSOVER           = "EMA_CROSSOVER"
    RSI_OVERBOUGHT_OVERSOLD = "RSI_OVERBOUGHT_OVERSOLD"
    BOLLINGER_BANDS         = "BOLLINGER_BANDS"
    MACD_CROSSOVER          = "MACD_CROSSOVER"
    BREAKOUT                = "BREAKOUT"
    MOVING_AVERAGE_ENVELOPE = "MOVING_AVERAGE_ENVELOPE"
    DONCHIAN_CHANNEL        = "DONCHIAN_CHANNEL"

