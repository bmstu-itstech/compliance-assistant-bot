from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime, Text, Boolean, Enum

from core import domain
from services.db.base import Base


class BaseModel(Base):
    __abstract__ = True

    id         = Column(BigInteger, primary_key=True)
    created_on = Column(DateTime,   default=datetime.now)
    updated_on = Column(DateTime,   default=datetime.now, onupdate=datetime.now)


class User(BaseModel):
    __tablename__ = "users"

    username       = Column(Text,              nullable=True)
    is_bot_blocked = Column(Boolean,           nullable=False, default=False)
    role           = Column(Enum(domain.Role), nullable=False)

    @classmethod
    def from_domain(cls, user: domain.User) -> "User":
        return User(**user.__dict__)

    def to_domain(self) -> domain.User:
        return domain.User(
            id=self.id,
            is_bot_blocked=self.is_bot_blocked,
            role=self.role,
            username=self.username
        )
