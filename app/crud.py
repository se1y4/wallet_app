from typing import cast
from sqlalchemy.orm import Session
from sqlalchemy import text
from app import models, schemas
from decimal import Decimal

def get_wallet(db: Session, wallet_id: str):
    return db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()

def create_wallet(db: Session, wallet_id: str):
    db_wallet = models.Wallet(id=wallet_id, balance=Decimal('0.00'))
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

def perform_operation(db: Session, wallet_id: str, operation: schemas.OperationCreate):
    # Используем SELECT FOR UPDATE для предотвращения race condition
    wallet = db.execute(
        text("SELECT * FROM wallets WHERE id = :wallet_id FOR UPDATE"),
        {"wallet_id": wallet_id}
    ).fetchone()
    
    if not wallet:
        wallet = create_wallet(db, wallet_id)
        wallet = (wallet.id, wallet.balance)
    else:
        # Преобразуем результат в объект для удобства работы
        wallet = (wallet[0], wallet[1])  # id, balance
    
    current_balance = Decimal(str(wallet[1])) if wallet[1] else Decimal('0.00')
    amount = Decimal(str(operation.amount))
    
    if operation.operation_type == "WITHDRAW" and current_balance < amount:
        raise ValueError("Insufficient funds")
    
    # Рассчитываем новый баланс
    if operation.operation_type == "DEPOSIT":
        new_balance = current_balance + amount
    else:  # WITHDRAW
        new_balance = current_balance - amount
    
    # Обновляем баланс кошелька
    db.execute(
        text("UPDATE wallets SET balance = :balance WHERE id = :wallet_id"),
        {"balance": float(new_balance), "wallet_id": wallet_id}
    )
    
    # Создаем запись об операции
    db_operation = models.Operation(
        wallet_id=wallet_id,
        operation_type=operation.operation_type,
        amount=amount
    )
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    
    return db_operation

def get_wallet_balance(db: Session, wallet_id: str):
    wallet = get_wallet(db, wallet_id)
    if not wallet:
        wallet = create_wallet(db, wallet_id)
    return wallet