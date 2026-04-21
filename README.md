# py-common-lib

複数プロジェクトで共有する Python ライブラリ。制約付き HTTP クライアントやシークレットストアなどの共通ユーティリティを提供する。

詳細は [docs/overview.md](docs/overview.md) を参照。

## セットアップ

```bash
uv sync
```

## テスト

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```
