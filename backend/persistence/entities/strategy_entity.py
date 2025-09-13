from sqlalchemy import Column, Integer, String, JSON, Boolean, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from database import Base
from persistence.entities.utils_entity import StrategyType


class StrategyEntity(Base):
    __tablename__ = 'strategies'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    type        = Column(Enum(StrategyType), nullable=False)
    parameters  = Column(JSON, nullable=True)

    created_by  = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    is_public   = Column(Boolean, default=True)
    created_at  = Column(TIMESTAMP, default="NOW()")

    user        = relationship("UserEntity",        back_populates="strategies")
    backtests   = relationship("BacktestEntity",    back_populates="strategy", cascade="all, delete-orphan")
