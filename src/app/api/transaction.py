from app.api import crud
from app.api.models import TransactionSchema, TransactionDB
from fastapi import APIRouter

router = APIRouter()


@router.post("/", response_model=TransactionDB, status_code=201)
async def create_transaction(payload: TransactionSchema):
    created_transaction = await crud.post_transaction(payload)
    return created_transaction;


@router.get("/", response_model=list[TransactionDB], status_code=200)
async def get_transactions():
    return await crud.get_all_transactions()


@router.put("/transfer", status_code=200)
async def create_transfer(payload: TransactionSchema):
    return await crud.create_transfer(payload)
