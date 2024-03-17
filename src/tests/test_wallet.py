from app.api import crud


def test_get_wallet_balance(test_app, monkeypatch):
    test_response = {"balance": {"btc": 2.9052220010155345, "eur": 182751.9746220346}}

    async def mock_get_wallet_balance():
        return test_response

    monkeypatch.setattr(crud, "get_wallet_balance", mock_get_wallet_balance)

    response = test_app.get("/wallet/")
    assert response.status_code == 200
    assert response.json() == test_response
