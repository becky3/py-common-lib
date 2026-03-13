# py-common-lib

複数プロジェクトで共有する Python ライブラリ。制約付き HTTP クライアント（バジェット・サーキットブレーカー・レート制限）を提供する。

## パッケージ構造

| パッケージ | 概要 |
|-----------|------|
| `py_common_lib.core` | HTTP 非依存のコアコンポーネント（BudgetTracker, CircuitBreaker） |
| `py_common_lib.httpx` | httpx 用の制約付き HTTP クライアント（ConstrainedClient） |

## 動作環境

- Python 3.11+
- パッケージ管理: uv

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

## Git 運用

main ブランチのみで運用する。直接 push は不可、全ての変更は PR 経由で行う。

## 開発ガイドライン

**開発を始める前に必ず [CLAUDE.md](CLAUDE.md) を読んでください。**

## 関連

- [rag-knowledge](https://github.com/becky3/rag-knowledge) — 最初の利用先プロジェクト
