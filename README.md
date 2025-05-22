# アーキテクチャ検討サンドボックス

このプロジェクトは [OpenAPI Generator](https://openapi-generator.tech) により自動生成された FastAPI サーバーをベースに、独自のアーキテクチャで拡張・開発しています。(ベース: ポート&アダプタ)

- API バージョン: 1.0.0
- ジェネレーター バージョン: 7.13.0-SNAPSHOT
- ビルドパッケージ: org.openapitools.codegen.languages.PythonFastAPIServerCodegen

## 必要要件

- Python 3.12 以上（ご利用の環境に合わせて調整してください）
- Linux (x86_64)
- Docker / Docker Compose
- [uv](https://github.com/astral-sh/uv)（ローカル開発時のみ）

## ディレクトリ構成

- `openapi_server/` : FastAPI アプリ本体
- `tests/` : テストコード
- `openapi.yaml` : OpenAPI 定義
- `Dockerfile`, `docker-compose.yaml` : Docker 関連
- `pyproject.toml`, `uv.lock` : Python依存管理

## 環境構築方法（ローカル開発用）

1. [uv](https://github.com/astral-sh/uv) をインストールしてください。
   ```bash
   curl -Ls https://astral.sh/uv/install.sh | sh
   # もしくは各種パッケージマネージャでインストール
   ```
2. 依存パッケージをインストールします。
   ```bash
   uv venv
   uv sync
   ```

## サーバーの起動方法（Docker Compose 推奨）

以下のコマンドでアプリケーションとDBをまとめて起動できます。

```bash
docker compose up --build
```

- API: http://localhost:8080/docs でドキュメントを確認できます。
- DB: PostgreSQL（localhost:5432, DB名: todo）

## テストの実行方法

ローカルでテストを実行する場合は、uv環境で以下を実行してください。

```bash
uv pip install pytest
PYTHONPATH=src pytest tests
```

---

何か問題が発生した場合は、Python のバージョンや依存パッケージ、OS 環境（Linux x86_64）、Docker/uvのバージョンを確認してください。
