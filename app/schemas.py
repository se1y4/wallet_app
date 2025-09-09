from pydantic import BaseModel
from typing import Union
from decimal import Decimal
import uuid

class OperationCreate(BaseModel):
    operation_type: str
    amount: Decimal

    class Config:
        from_attributes = True

class WalletResponse(BaseModel):
    id: str
    balance: Decimal

    class Config:
        from_attributes = True

class OperationResponse(BaseModel):
    id: int
    wallet_id: str
    operation_type: str
    amount: Decimal
    created_at: str

    class Config:
        from_attributes = True