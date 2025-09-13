from sqlalchemy import Column, Integer, TIMESTAMP, JSON, ForeignKey, String, func, Boolean
from sqlalchemy.orm import relationship
from database import Base


class StatisticEntity(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    name = Column(String, nullable=False)
    params = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    user = relationship("UserEntity", back_populates="statistics")