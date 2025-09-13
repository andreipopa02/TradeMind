from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base


class EventEntity(Base):
    __tablename__ = 'events'

    id              = Column(Integer, primary_key=True)
    user_id         = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    title           = Column(String(255), nullable=False)
    description     = Column(Text)
    category        = Column(String(50))
    start_time      = Column(TIMESTAMP, nullable=False)
    end_time        = Column(TIMESTAMP, nullable=False)
    location        = Column(String(255))
    reminder_time   = Column(TIMESTAMP)
    created_at      = Column(TIMESTAMP, default="NOW()")

    user = relationship("UserEntity", back_populates="events")
