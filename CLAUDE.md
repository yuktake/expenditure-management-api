# CLAUDE.md - MyWallets API 開発規則

このファイルは、MyWallets API プロジェクトにおける開発規則、コーディング規約、アーキテクチャパターンを定義します。

## アーキテクチャ

### クリーンアーキテクチャ

本プロジェクトはクリーンアーキテクチャの原則に従います：

```
API層 (api/) → ユースケース層 (usecases/) → リポジトリ層 (repositories/) → モデル層 (models/)
```

**依存関係の方向**:
- 依存関係は内側に向かって流れる
- 外側の層は内側の層に依存するが、内側の層は外側の層を知らない
- 抽象インターフェースを使用して依存関係を逆転させる

### プロジェクト構成

```
app/
├── api/                    # API層：HTTPリクエストの処理
│   ├── admin/             # 管理者機能
│   ├── auth/              # 認証機能
│   ├── users/             # ユーザー管理
│   └── wallets/           # ウォレット管理
├── models/                # データモデル
│   ├── alchemy/           # SQLAlchemy ORM モデル
│   └── pydantic/          # Pydantic ビジネスモデル
├── repositories/          # データアクセス層
├── usecases/             # ビジネスロジック層
├── dependencies/         # 依存性注入設定
├── session/              # データベースセッション管理
├── utils/                # ユーティリティ
└── tests/                # テストコード
```

## コーディング規約

### ファイル・ディレクトリ命名

- **snake_case**: すべてのファイル・ディレクトリ名は snake_case
- **接尾辞パターン**:
  - `*_repository.py`: データアクセス層
  - `*_usecase.py`: ビジネスロジック層
  - `*_views.py`: API エンドポイント
  - `*_schemas.py`: API データモデル
  - `test_*.py`: テストファイル

### クラス命名

- **PascalCase**: すべてのクラス名は PascalCase
- **接尾辞パターン**:
  - `*ORM`: SQLAlchemy モデル (`WalletORM`, `UserORM`)
  - `Abstract*`: 抽象基底クラス (`AbstractWalletRepository`)
  - `*Interface`: 依存性注入用型 (`WalletRepositoryInterface`)
  - `*Request/*Response`: API スキーマ (`PostWalletRequest`)

### 関数・変数命名

- **snake_case**: すべての関数・変数名は snake_case
- **説明的な名前**: 機能を明確に表す名前を使用

### インポート順序

```python
# 1. 標準ライブラリ
from datetime import datetime
from typing import Optional

# 2. サードパーティライブラリ
from fastapi import APIRouter, Query, status
from sqlalchemy import select

# 3. ローカルインポート
from models.pydantic.wallet import Wallet
from dependencies.usecase import ListWalletsInterface
```

## データモデル規約

### デュアルモデルアプローチ

- **SQLAlchemy モデル** (`models/alchemy/`): データベース操作用
- **Pydantic モデル** (`models/pydantic/`): ビジネスロジック・API シリアライゼーション用

### モデル変換

```python
# ORM → Entity 変換
def to_entity(self) -> Wallet:
    return Wallet(
        wallet_id=self.wallet_id,
        name=self.name,
        balance=self.balance
    )

# Entity → ORM 変換
@classmethod
def from_entity(cls, wallet: Wallet) -> WalletORM:
    return cls(
        wallet_id=wallet.wallet_id,
        name=wallet.name,
        balance=wallet.balance
    )
```

## 依存性注入規約

### インターフェース基盤設計

```python
# 抽象インターフェース定義
class AbstractWalletRepository:
    async def find_by_id(self, wallet_id: int) -> Wallet:
        raise NotImplementedError

# 依存性注入での型指定
WalletRepositoryInterface = Annotated[
    AbstractWalletRepository,
    Depends(get_wallet_repository)
]
```

### 環境別実装

```python
def get_wallet_repository() -> AbstractWalletRepository:
    if settings.status == "testing":
        return TestWalletRepository()
    return WalletRepository()
```

## データベース操作規約

### セッション管理

```python
# 読み取り専用操作
async with sess() as s:
    result = await s.execute(select(WalletORM))

# 書き込み操作（トランザクション）
async with sess.begin() as s:
    s.add(wallet_orm)
    await s.commit()
```

### リポジトリパターン

- すべてのリポジトリは抽象基底クラスを実装
- 非同期操作を使用
- データベースセッションは依存性注入で提供

## API 設計規約

### RESTful 設計

- **リソースベース URL**: `/api/v1/wallets/{wallet_id}`
- **適切な HTTP メソッド**: GET, POST, PUT, DELETE
- **適切なステータスコード**:
  - `200`: 成功
  - `201`: 作成成功
  - `204`: 削除成功
  - `400`: バリデーションエラー
  - `404`: リソースが見つからない
  - `500`: サーバーエラー

### リクエスト/レスポンスモデル

```python
class PostWalletRequest(BaseModel):
    name: str

class PostWalletResponse(Wallet):
    pass
```

### API バージョニング

- URL でのバージョニング: `/api/v1/`

## エラーハンドリング規約

### カスタム例外階層

```python
class AppException(Exception):
    status_code: int = 500
    message: str = "Internal Server Error"
    details: dict | None = None

class NotFound(AppException):
    status_code = 404
    message: str = "Not Found"
```

### エラーレスポンス形式

```json
{
    "message": "エラーメッセージ",
    "details": {
        "field": "具体的なエラー詳細"
    }
}
```

## テスト規約

### テスト構成

- **pytest + anyio**: 非同期テスト用
- **テストフィクスチャ**: `conftest.py` で一元管理
- **命名規則**: `test_*.py` ファイル、`test_*` 関数

### テスト実装パターン

```python
@pytest.mark.anyio
async def test_get_wallets(ac):
    response = await ac.get("/api/v1/wallets")
    assert response.status_code == 200
    assert response.json() == expected_response
```

### テストダブル戦略

- 本番とは別のテスト実装を作成 (`TestWalletRepository`, `TestWalletUsecase`)
- モックよりも実装による置き換えを優先
- 環境変数 `settings.status == "testing"` でテスト用実装に切り替え

## 設定管理規約

### Pydantic Settings

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='allow')
```

### 環境別動作

- `settings.status` による動作切り替え
- テスト環境では専用実装を使用

## コードスタイル規約

### 型ヒント

- 全ての関数・メソッドに型ヒントを記述
- `Annotated` 型を依存性注入で活用
- Python 3.11+ の新しい Union 記法 (`|`) を使用

### 非同期プログラミング

- データベース操作は全て非同期
- API から データベースまで一貫して async/await を使用

### ドキュメント

- API エンドポイントには説明的な docstring
- 複雑なロジックには適切なコメント
- Pydantic モデルのフィールドには説明を記述

## セキュリティ規約

### API 認証

- 全ての API リクエストに `APP-API-KEY` ヘッダーが必要
- セッション Cookie による追加認証
- Cognito トークンの検証（TODO として実装予定）

### データ保護

- 機密情報のログ出力を禁止
- 環境変数による設定管理
- SQL インジェクション対策（SQLAlchemy ORM 使用）

## 開発ワークフロー

### テスト実行

```bash
cd app
poetry run pytest
```

### 開発サーバー起動

```bash
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### Docker 環境

```bash
docker-compose up --build
```

## 重要な原則

1. **関心の分離**: 各層は明確な責任を持つ
2. **依存関係の逆転**: 抽象に依存し、具象に依存しない
3. **テスタビリティ**: 全てのコンポーネントがテスト可能
4. **型安全性**: 型ヒントによる静的解析サポート
5. **非同期性**: パフォーマンスのための一貫した非同期実装
6. **拡張性**: 新機能追加時の影響を最小化

このドキュメントに従って開発することで、保守性・テスタビリティ・拡張性の高いコードベースを維持できます。