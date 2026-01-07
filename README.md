# Scheduler Project

寮のスケジュール管理システム (Domitory Scheduler)

## 技術スタック

### Frontend

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **UI Library**: Material UI (v7)
- **Data Fetching**: SWR, Axios
- **State/Utils**: Dayjs

### Backend

- **Framework**: FastAPI (Python)
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Migration**: Alembic

### Infrastructure

- **Containerization**: Docker, Docker Compose

## 開発環境のセットアップ

### 前提条件

- Docker
- Docker Compose

### 起動方法

コンテナをビルドして起動します。

```bash
docker compose up --build
```

### アクセス

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8888
- **API Documentation (Swagger UI)**: http://localhost:8888/docs

## ディレクトリ構成

- `next/`: フロントエンド (Next.js) ソースコード
- `api/`: バックエンド (FastAPI) ソースコード
  - `ddd/`: エンティティなど
  - `migrations/`: Alembic マイグレーションファイル
- `docker/`: Docker ビルド用の設定ファイル
- `scripts/`: コンテナ起動用スクリプト
- `manage/`: 管理用スクリプト (DB 初期化等)

## 管理コマンド

### データベース初期化

(詳細な手順は `manage/` ディレクトリ配下のスクリプトを参照)

```bash
# 例: apiコンテナ内で実行
uv run python manage/initdb.py
```

### マイグレーション

Database の変更を反映する場合 (api コンテナ内で実行):

```bash
uv run alembic upgrade head
```
