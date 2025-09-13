from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from database import Base

from persistence.entities.strategy_entity import StrategyEntity

class BacktestEntity(Base):
    __tablename__ = 'backtests'

    id           = Column(Integer, primary_key=True)
    user_id      = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    strategy_id  = Column(Integer, ForeignKey('strategies.id', ondelete='SET NULL'))

    symbol       = Column(String(20), nullable=False)
    time_frame   = Column(String(20), nullable=False)
    start_date   = Column(TIMESTAMP)
    end_date     = Column(TIMESTAMP)

    initial_balance = Column(Float, nullable=True)
    risk_per_trade  = Column(Float, nullable=True)

    total_profit    = Column(Float, nullable=True)
    drawdown_max    = Column(Float, nullable=True)
    winrate         = Column(Float, nullable=True)
    nr_trades       = Column(Integer, nullable=True)
    profit_factor   = Column(Float, nullable=True)
    expectancy      = Column(Float, nullable=True)
    balance_curve   = Column(JSONB, nullable=True)

    created_at      = Column(TIMESTAMP, default="NOW()")
    name            = Column(String(150), nullable=True)

    user            = relationship("UserEntity",        back_populates="backtests")
    strategy        = relationship("StrategyEntity",    back_populates="backtests")
    trades          = relationship("TradeEntity",       back_populates="backtest", cascade="all, delete-orphan")

