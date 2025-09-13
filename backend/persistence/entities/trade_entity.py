from sqlalchemy import Column, Integer, String, Date, Time, Numeric, Enum, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

from persistence.entities.utils_entity import TradeType, SourceType, SessionType


class TradeEntity(Base):
    __tablename__ = 'trades'

    # Identifying part
    id          = Column(Integer, primary_key=True, autoincrement=True)
    user_id     = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Essential part
    market      = Column(String(20), nullable=False)
    volume      = Column(Numeric(10, 2), nullable=False)
    type        = Column(Enum(TradeType), nullable=False)

    # Time part
    open_date   = Column(Date, nullable=False)
    open_time   = Column(Time, nullable=False)
    close_date  = Column(Date, nullable=True)
    close_time  = Column(Time, nullable=True)
    session     = Column(Enum(SessionType), nullable=False)

    # Price part
    open_price  = Column(Numeric(14, 5), nullable=False)
    close_price = Column(Numeric(14, 5), nullable=True)
    sl_price    = Column(Numeric(14, 5), nullable=True)
    tp_price    = Column(Numeric(14, 5), nullable=True)

    # Money part
    swap        = Column(Numeric(12, 2), nullable=True)
    commission  = Column(Numeric(12, 2), nullable=True)
    profit      = Column(Numeric(12, 2), nullable=True)
    pips        = Column(Numeric(12, 2), nullable=True)

    # Photo link
    link_photo  = Column(String(150),                  nullable=True)

    source_type = Column(Enum(SourceType),             nullable=False)
    backtest_id = Column(Integer, ForeignKey("backtests.id", ondelete="CASCADE"), nullable=True)

    user        = relationship("UserEntity",        back_populates="trades")
    backtest    = relationship("BacktestEntity",    back_populates="trades")