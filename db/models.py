import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Boolean, Text, func, Integer, ForeignKey, BigInteger, Enum
from sqlalchemy.orm import relationship

from utils import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    phone_number = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True)  # Add this
    is_phone_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)  # Add this for admin access
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))


    def __repr__(self):
        return f"{self.id} {self.name} {self.is_active}"