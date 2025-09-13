from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from database import Base


class TradingAccountEntity(Base):
    __tablename__ = "trading_accounts"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    broker_name = Column(String, nullable=False)
    account_id  = Column(BigInteger, unique=True, nullable=False)
    server      = Column(String, nullable=True)
    password    = Column(String, nullable=False)

    user        = relationship("UserEntity", back_populates="trading_accounts")
