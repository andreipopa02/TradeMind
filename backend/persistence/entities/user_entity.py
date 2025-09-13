from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

from persistence.entities.backtest_entity import BacktestEntity
from persistence.entities.statistic_entity import StatisticEntity

class UserEntity(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String, nullable=False)
    last_name  = Column(String, nullable=False)
    email      = Column(String, unique=True, index=True, nullable=False)
    password   = Column(String, nullable=False)

    phone      = Column(String, nullable=False)
    gender     = Column(String, nullable=True)
    country    = Column(String, nullable=False)

    is_verified = Column(Boolean, default=False)

    trading_accounts    = relationship("TradingAccountEntity",  back_populates="user", cascade="all, delete-orphan")
    trades              = relationship("TradeEntity",           back_populates="user", cascade="all, delete-orphan")
    backtests           = relationship("BacktestEntity",        back_populates="user", cascade="all, delete-orphan")
    strategies          = relationship("StrategyEntity",        back_populates="user", cascade="all, delete-orphan")
    statistics          = relationship("StatisticEntity",       back_populates="user", cascade="all, delete-orphan")
