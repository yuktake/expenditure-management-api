from datetime import datetime

import pytest

from models.pydantic.wallet import Wallet
from models.pydantic.history import History, HistoryType

def test_wallet_balance():
    wallet = Wallet(
        wallet_id=999,
        name="Aaron",
        histories=[
            History(
                history_id=1,
                name="test_history1",
                amount=500,
                type=HistoryType.INCOME,
                history_at=datetime(2021,12,24,3,30,20),
                wallet_id=999
            ),
            History(
                history_id=2,
                name="test_history2",
                amount=100,
                type=HistoryType.OUTCOME,
                history_at=datetime(2021,12,24,3,30,20),
                wallet_id=999
            ),
        ]
    )

    assert wallet.balance == 400

def test_wallet_name_validation():
    with pytest.raises(ValueError) as e:
        Wallet(
            wallet_id=999,
            name="test",
            histories=[]
        )

        # エラーメッセージを検証
        assert "test is not allowed" in str(e.value)