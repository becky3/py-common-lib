# py-common-lib

複数プロジェクトで共有する Python ライブラリ。制約付き HTTP クライアントやシークレットストアなどの共通ユーティリティを提供する。

## パッケージ構造

| パッケージ | 概要 |
| ----------- | ------ |
| `py_common_lib.core` | HTTP 非依存のコアコンポーネント（BudgetTracker, CircuitBreaker） |
| `py_common_lib.httpx` | httpx 用の制約付き HTTP クライアントとクランプユーティリティ |
| `py_common_lib.secrets` | OS セキュアストレージからのシークレット取得（keyring） |

## 動作環境

- Python 3.11+
- パッケージ管理: uv

## テスト

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

## Git 運用

main ブランチのみで運用する。develop ブランチは使用しない。

- 作業ブランチ: `feature/{機能名}-#{Issue番号}` / `bugfix/{修正内容}-#{Issue番号}` を main から作成
- PR の base: `main`
- 直接 push は不可、全ての変更は PR 経由で行う
