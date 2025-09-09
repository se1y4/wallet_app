from fastapi import FastAPI
from app.api.v1.endpoints import wallets
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wallet API", version="1.0.0")

app.include_router(wallets.router, prefix="/api/v1/wallets", tags=["wallets"])

@app.get("/")
async def root():
    return {"message": "Wallet API"}