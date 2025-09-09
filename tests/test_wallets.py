import pytest
from fastapi.testclient import TestClient
from app.main import app
from decimal import Decimal
import uuid

client = TestClient(app)

@pytest.fixture
def wallet_id():
    return str(uuid.uuid4())

def test_create_wallet_and_get_balance(wallet_id):
    # Получаем баланс несуществующего кошелька (он будет создан)
    response = client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == wallet_id
    assert Decimal(str(data["balance"])) == Decimal("0.00")

def test_invalid_wallet_uuid():
    response = client.get("/api/v1/wallets/invalid-uuid")
    assert response.status_code == 400

def test_deposit_operation(wallet_id):
    # Пополнение счета
    operation_data = {
        "operation_type": "DEPOSIT",
        "amount": "1000.50"
    }
    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json=operation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["wallet_id"] == wallet_id
    assert data["operation_type"] == "DEPOSIT"
    assert Decimal(str(data["amount"])) == Decimal("1000.50")

    # Проверяем баланс
    response = client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 200
    data = response.json()
    assert Decimal(str(data["balance"])) == Decimal("1000.50")

def test_withdraw_operation(wallet_id):
    # Снятие средств
    operation_data = {
        "operation_type": "WITHDRAW",
        "amount": "500.25"
    }
    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json=operation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["wallet_id"] == wallet_id
    assert data["operation_type"] == "WITHDRAW"
    assert Decimal(str(data["amount"])) == Decimal("500.25")

    # Проверяем баланс
    response = client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 200
    data = response.json()
    assert Decimal(str(data["balance"])) == Decimal("500.25")

def test_insufficient_funds(wallet_id):
    # Пытаемся снять больше, чем есть
    operation_data = {
        "operation_type": "WITHDRAW",
        "amount": "1000.00"
    }
    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json=operation_data)
    assert response.status_code == 400

def test_invalid_operation_type(wallet_id):
    operation_data = {
        "operation_type": "INVALID",
        "amount": "100.00"
    }
    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json=operation_data)
    assert response.status_code == 400

def test_negative_amount(wallet_id):
    operation_data = {
        "operation_type": "DEPOSIT",
        "amount": "-100.00"
    }
    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json=operation_data)
    assert response.status_code == 400

def test_concurrent_operations(wallet_id):
    import threading
    import time
    
    def deposit_operation():
        operation_data = {
            "operation_type": "DEPOSIT",
            "amount": "100.00"
        }
        client.post(f"/api/v1/wallets/{wallet_id}/operation", json=operation_data)
    
    # Запускаем несколько потоков одновременно
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=deposit_operation)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Проверяем, что все операции прошли успешно
    response = client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 200
    data = response.json()
    # Баланс должен быть 500.00 (5 операций по 100.00)
    assert Decimal(str(data["balance"])) == Decimal("500.00")