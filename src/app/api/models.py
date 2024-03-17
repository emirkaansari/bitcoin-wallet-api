import secrets
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class Amount(BaseModel):
    btc: float
    eur: float


class AccountBalanceSchema(BaseModel):
    balance: Amount


class TransferSchema(BaseModel):
    transferred_amount: Amount
    new_balance: AccountBalanceSchema


class TransactionSchema(BaseModel):
    amount: float


class TransactionDB(TransactionSchema):
    id: str = Field(default_factory=lambda: TransactionDB.generate_unique_hex_string(16))
    spent: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    @staticmethod
    def generate_unique_hex_string(length):
        unique_id = uuid.uuid4().hex
        random_hex = secrets.token_hex(length // 2)
        unique_hex_string = unique_id + random_hex
        return unique_hex_string[:length]
