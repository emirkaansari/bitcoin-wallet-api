import json

from app.api import crud
from fastapi import HTTPException


def test_transaction_post(test_app, monkeypatch):
    test_request_payload = {"amount": 10.2}
    test_value = {"id": "21a45rgt", "amount": 10.2, "spent": False, "created_at": "2024-03-17T12:13:15.544514"}

    async def mock_post_transaction(payload):
        return test_value

    monkeypatch.setattr(crud, "post_transaction", mock_post_transaction)

    response = test_app.post("/transaction/",
                             content=json.dumps(test_request_payload))  # Use POST for creating a resource
    assert response.status_code == 201
    assert response.json() == test_value


def test_transaction_post_invalid_payload(test_app):
    response = test_app.post("/transaction/", content=json.dumps({"f": 10.2}))
    assert response.status_code == 422


def test_get_all_transactions(test_app, monkeypatch):
    test_value = [
        {"id": "21a45rgt", "amount": 10.2, "spent": False, "created_at": "2024-03-17T12:13:15.544514"},
        {"id": "23a45rar", "amount": 10.3, "spent": False, "created_at": "2024-03-16T12:13:15.544514"}
    ]

    async def mock_get_all():
        return test_value

    monkeypatch.setattr(crud, "get_all_transactions", mock_get_all)
    response = test_app.get("/transaction/")
    assert response.status_code == 200
    assert response.json() == test_value


def test_create_transfer(test_app, monkeypatch):
    test_request_payload = {"amount": 10.2}

    test_response = {
        "transferred_amount": {
            "btc": 0.00016303741712076376,
            "eur": 10.2
        },
        "new_balance": {
            "balance": {
                "btc": 2.9052220010155345,
                "eur": 181757.44521522158
            }
        }
    }

    async def mock_create_transfer(payload):
        return test_response

    monkeypatch.setattr(crud, "create_transfer", mock_create_transfer)

    response = test_app.put("/transaction/transfer/", content=json.dumps(test_request_payload))
    assert response.status_code == 200
    assert response.json() == test_response


def test_create_transfer_less_than_required_money(test_app, monkeypatch):
    test_request_payload = {"amount": 0.01}
    test_response = {"detail": "Transfers can't be less than 0.00001 BTC."}

    async def mock_create_transfer(payload):
        raise HTTPException(status_code=400, detail="Transfers can't be less than 0.00001 BTC.")

    monkeypatch.setattr(crud, "create_transfer", mock_create_transfer)

    response = test_app.put("/transaction/transfer/", content=json.dumps(test_request_payload))
    assert response.status_code == 400
    assert response.json() == test_response


def test_create_transfer_over_the_balance(test_app, monkeypatch):
    test_request_payload = {"amount": 23123132112}
    test_response = {"detail": "There is not enough money in the wallet for this transfer."}

    async def mock_create_transfer(payload):
        raise HTTPException(status_code=400, detail="There is not enough money in the wallet for this transfer.")

    monkeypatch.setattr(crud, "create_transfer", mock_create_transfer)

    response = test_app.put("/transaction/transfer/", content=json.dumps(test_request_payload))
    assert response.status_code == 400
    assert response.json() == test_response
