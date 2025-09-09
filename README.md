# Wallet API

API для управления кошельками с поддержкой конкурентных операций.

## Технологии

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (миграции)
- Docker & Docker Compose
- Pytest (тестирование)

## Запуск приложения

### С помощью Docker Compose

```bash
docker-compose up --build
```
Запуск тестов
```bash
docker-compose exec app pytest
```
Приложение будет доступно по адресу: http://localhost:8000
