from typing import List

from app.api.models import TransactionSchema, TransactionDB, \
    AccountBalanceSchema, Amount, TransferSchema
from app.api.util import bitcoin
from app.db import database, transaction
from fastapi import HTTPException
from sqlalchemy import select, func


async def post_transaction(payload: TransactionSchema):
    transaction_db = TransactionDB(**payload.dict())
    query = transaction.insert() \
        .values(id=transaction_db.id,
                amount=payload.amount,
                spent=transaction_db.spent,
                created_date=transaction_db.created_at)

    await database.execute(query=query)
    return transaction_db


async def get_all_transactions():
    query = transaction.select()
    result = await database.fetch_all(query=query)

    transactions: List[TransactionDB] = [
        TransactionDB(**row) for row in result
    ]
    return transactions


async def get_wallet_balance():
    query = select(func.sum(transaction.c.amount)) \
        .where(transaction.c.spent == False)

    btc_val = await database.execute(query=query)
    euro_val = await bitcoin.convert_btc_to_eur(btc_val)

    return AccountBalanceSchema(balance=Amount(btc=btc_val, eur=euro_val))


async def create_transfer(payload: float):
    # Check Balance if not enough reject the request with a message not enough balance

    current_balance = await get_wallet_balance()
    if current_balance.balance.eur < payload.amount:
        raise HTTPException(status_code=400, detail="There is not enough money in the wallet for this transfer.")

    # convert
    amount_btc = await bitcoin.convert_eur_to_btc(payload.amount)
    if amount_btc < 0.00001:
        raise HTTPException(status_code=400, detail="Transfers can't be less than 0.00001 BTC.")

    remaining_amount = amount_btc

    query = select(transaction) \
        .filter(transaction.c.spent == False) \
        .order_by(transaction.c.amount.desc())
    unspent_transactions = await database.fetch_all(query=query)

    transaction_ids = []
    for trans in unspent_transactions:
        if trans.amount >= remaining_amount:
            transaction_ids.append(trans.id)
            break
        else:
            transaction_ids.append(trans.id)
            remaining_amount -= trans.amount

    # Update spent status
    if transaction_ids:
        query = transaction.update().where(transaction.c.id.in_(transaction_ids)) \
            .values(spent=True)
        await database.execute(query=query)

    # Create a new transaction if necessary
    if remaining_amount > 0:
        transaction_db = TransactionDB(amount=remaining_amount)
        query = transaction.insert() \
            .values(id=transaction_db.id,
                    amount=transaction_db.amount,
                    spent=False,
                    created_date=transaction_db.created_at)
        await database.execute(query=query)

    new_balance_data = await get_wallet_balance()

    return TransferSchema(transferred_amount=Amount(btc=amount_btc, eur=payload.amount)
                          , new_balance=new_balance_data)
