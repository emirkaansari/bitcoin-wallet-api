from app.api import transaction, wallet
from app.db import engine, database, metadata
from fastapi import FastAPI

metadata.create_all(engine)

app = FastAPI(root_path="/v1")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(transaction.router, prefix="/transaction", tags=["transaction"])
app.include_router(wallet.router, prefix="/wallet", tags=["wallet"])
