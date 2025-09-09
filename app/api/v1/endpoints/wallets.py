from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
import uuid

router = APIRouter()

@router.post("/{wallet_uuid}/operation", response_model=schemas.OperationResponse)
def perform_wallet_operation(
    wallet_uuid: str,
    operation: schemas.OperationCreate,
    db: Session = Depends(get_db)
):
    try:
        # Проверяем корректность UUID
        try:
            uuid.UUID(wallet_uuid)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid wallet UUID")
        
        # Проверяем корректность типа операции
        if operation.operation_type not in ["DEPOSIT", "WITHDRAW"]:
            raise HTTPException(status_code=400, detail="Invalid operation type")
        
        # Проверяем корректность суммы
        if operation.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        
        db_operation = crud.perform_operation(db, wallet_uuid, operation)
        return db_operation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{wallet_uuid}", response_model=schemas.WalletResponse)
def get_wallet_balance(
    wallet_uuid: str,
    db: Session = Depends(get_db)
):
    try:
        uuid.UUID(wallet_uuid)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid wallet UUID")
    
    wallet = crud.get_wallet_balance(db, wallet_uuid)
    return wallet