import pytest
from datetime import datetime
from models import Wallet, HistoryType

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

@pytest.mark.anyio
async def test_get_wallet(ac):
    response =  await ac.get("/api/v1/wallets/1")
    assert response.status_code == 200
    assert response.json() == {
        "wallet_id": 999,
        "name": "testing",
        "balance": 100,
    }

@pytest.mark.anyio
async def test_get_wallet_with_histories(ac):
    response =  await ac.get("/api/v1/wallets/1?include_histories=true")
    assert response.status_code == 200
    assert response.json() == {
        "wallet_id": 999,
        "name": "testing",
        "balance": 100,
        "histories": [
            {
                "history_id": 999,
                "name": "test_history",
                "amount": 100,
                "type": HistoryType.INCOME,
                "history_at": "2021-12-24T03:30:20Z"
            }
        ]
    }

@pytest.mark.anyio
async def test_post_wallet(ac):
    response =  await ac.post("/api/v1/wallets", json={"name": "testing"})
    assert response.status_code == 201
    assert response.json() == {
        "wallet_id": 999,
        "name": "testing",
        "balance": 0,
    }

@pytest.mark.anyio
async def test_put_wallet(ac):
    response =  await ac.put("/api/v1/wallets/1", json={"name": "updated"})
    assert response.status_code == 200
    assert response.json() == {
        "wallet_id": 999,
        "name": "updated",
        "balance": 100,
    }

@pytest.mark.anyio
async def test_delete_wallet(ac):
    response =  await ac.delete("/api/v1/wallets/1")
    assert response.status_code == 204

@pytest.mark.anyio
async def test_get_histories(ac):
    response =  await ac.get("/api/v1/wallets/1/histories")
    assert response.status_code == 200
    assert response.json() == {
        "histories": [
            {
                "history_id": 999,
                "name": "test_history",
                "amount": 100,
                "type": HistoryType.INCOME,
                "history_at": "2021-12-24T03:30:20Z"
            }
        ]
    }

@pytest.mark.anyio
async def test_get_history(ac):
    response =  await ac.get("/api/v1/wallets/1/histories/1")
    assert response.status_code == 200
    assert response.json() == {
        "history_id": 999,
        "name": "test_history",
        "amount": 100,
        "type": HistoryType.INCOME,
        "history_at": "2021-12-24T03:30:20Z"
    }

@pytest.mark.anyio
async def test_post_history(ac):
    response =  await ac.post(
        "/api/v1/wallets/1/histories",
        json={
            "wallet_id": 1,
            "name": "posted",
            "amount": 999,
            "type": HistoryType.INCOME,
            "history_at": "2021-12-24T03:30:20Z",
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        "history_id": 1,
        "name": "posted",
        "amount": 999,
        "type": HistoryType.INCOME,
        "history_at": "2021-12-24T03:30:20Z"
    }

@pytest.mark.anyio
async def test_update_history(ac):
    response =  await ac.put(
        "/api/v1/wallets/1/histories/999",
        json={
            "name": "updated",
            "amount": 777,
            "type": HistoryType.INCOME,
            "history_at": "2021-12-24T03:30:20Z"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "history_id": 999,
        "name": "updated",
        "amount": 777,
        "type": HistoryType.INCOME,
        "history_at": "2021-12-24T03:30:20Z"
    }

@pytest.mark.anyio
async def test_delete_history(ac):
    response =  await ac.delete("/api/v1/wallets/1/histories/999")
    assert response.status_code == 204

@pytest.mark.anyio
async def test_move_history(ac):
    response =  await ac.post(
        "/api/v1/wallets/1/histories/1/move",
        json={
            "destination_id": 2,
        }
    )
    assert response.json() == {
        "history_id": 999,
        "name": "test_history",
        "amount": 100,
        "type": HistoryType.INCOME,
        "history_at": "2021-12-24T03:30:20Z",
    }