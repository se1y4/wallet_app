from sqlalchemy import Column, Integer, String, Numeric, DateTime, func, Enum
from app.database import Base
import enum

class OperationType(str, enum.Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String, primary_key=True, index=True)
    balance = Column(Numeric(precision=10, scale=2), default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    wallet_id = Column(String, index=True)
    operation_type = Column(Enum(OperationType))
    amount = Column(Numeric(precision=10, scale=2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())