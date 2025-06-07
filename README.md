# MyWallets API

FastAPIベースのウォレット管理システムです。ユーザー認証、ウォレット管理、取引履歴の管理機能を提供します。

## 機能

- ユーザー認証・認可システム
- ウォレット管理機能
- 取引履歴の記録・参照
- 管理者機能
- API認証（APIキー、セッションベース）

## 技術スタック

- **Framework**: FastAPI 0.100.0
- **Language**: Python 3.11
- **Database**: MySQL (aiomysql)
- **ORM**: SQLAlchemy 2.0.18
- **Container**: Docker & Docker Compose
- **Package Manager**: Poetry
- **Testing**: pytest
- **AWS Services**: boto3 (Cognito等)

## プロジェクト構成

```
app/
├── api/                    # API エンドポイント
│   ├── admin/             # 管理者API
│   ├── auth/              # 認証API
│   ├── users/             # ユーザーAPI
│   └── wallets/           # ウォレットAPI
├── models/                # データモデル
│   ├── alchemy/           # SQLAlchemy ORM モデル
│   └── pydantic/          # Pydantic モデル
├── repositories/          # データアクセス層
├── usecases/             # ビジネスロジック層
├── dependencies/         # 依存性注入
├── session/              # セッション管理
├── utils/                # ユーティリティ
└── tests/                # テストコード
```

## セットアップ

### 必要な環境

- Docker
- Docker Compose
- MySQL ネットワーク (`mysql_default`)

### 起動方法

1. リポジトリをクローン:
```bash
git clone <repository-url>
cd fastapi
```

2. Docker Compose でアプリケーションを起動:
```bash
docker-compose up --build
```

3. アプリケーションは `http://localhost:8080` でアクセス可能

### 環境変数

`.env` ファイルを作成し、必要な環境変数を設定してください。

## API仕様

### 認証

全てのAPIリクエストには `APP-API-KEY` ヘッダーが必要です:
```
APP-API-KEY: DUMMY-KEY
```

一部のエンドポイントではセッションCookieによる認証も必要です。

### エンドポイント

- `/api/auth/*` - 認証関連API
- `/api/users/*` - ユーザー管理API
- `/api/wallets/*` - ウォレット管理API
- `/api/admin/*` - 管理者API

詳細なAPI仕様は `/docs` (Swagger UI) または `/redoc` で確認できます。

## 開発

### ローカル開発環境

```bash
# 依存関係のインストール
cd app
poetry install

# 開発サーバーの起動
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### テスト実行

```bash
cd app
poetry run pytest
```

### データベースマイグレーション

アプリケーション起動時に自動的にデータベースとテーブルが作成されます。

## アーキテクチャ

本プロジェクトはクリーンアーキテクチャの原則に従った階層構造を採用しています:

- **API層** (`api/`): HTTPリクエストの処理
- **ユースケース層** (`usecases/`): ビジネスロジック
- **リポジトリ層** (`repositories/`): データアクセス
- **モデル層** (`models/`): データ構造の定義

## ライセンス

このプロジェクトのライセンスについては、リポジトリ管理者にお問い合わせください。