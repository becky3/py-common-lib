"""セキュアストレージからのシークレット取得.

仕様: docs/specs/infrastructure/secret-store.md
"""

from __future__ import annotations

import keyring
from keyring.errors import KeyringError

from py_common_lib.secrets.errors import SecretNotFoundError, SecretStoreError


def get_secret(key: str, service: str) -> str:
    """指定されたサービス名・キー名でセキュアストレージからシークレットを取得する.

    Args:
        key: シークレットのキー名（例: "OPENAI_API_KEY"）
        service: サービス名（例: "rag-knowledge"）

    Returns:
        取得したシークレット値

    Raises:
        SecretNotFoundError: 指定されたサービス名・キー名の組み合わせが未登録
        SecretStoreError: バックエンドへのアクセスに失敗
    """
    try:
        value = keyring.get_password(service, key)
    except KeyringError as e:
        msg = f"Failed to access secret store: {e}"
        raise SecretStoreError(msg) from e

    if value is None:
        msg = f"Secret not found: service={service!r}, key={key!r}"
        raise SecretNotFoundError(msg)

    return value
