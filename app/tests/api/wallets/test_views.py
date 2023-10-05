import pytest
from models import Wallet

@pytest.mark.anyio
async def test_get_wallets(ac):
    response =  await ac.get("/api/v1/wallets")
    assert response.status_code == 200
    assert response.json() == {
        "wallets": [
            {
                "wallet_id": 999,
                "name": "testing",
                "balance": 0,
            },
            {
                "wallet_id": 1000,
                "name": "testing2",
                "balance": 0,
            },
        ]
    }