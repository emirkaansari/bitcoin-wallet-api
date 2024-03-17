from app.api import crud
from app.api.models import AccountBalanceSchema
from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=AccountBalanceSchema, status_code=200)
async def get_wallet_balance():
    return await crud.get_wallet_balance()
