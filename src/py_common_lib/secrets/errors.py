"""シークレットストアのエラー型.

仕様: docs/specs/infrastructure/secret-store.md
"""


class SecretStoreError(Exception):
    """シークレットストア関連エラーの基底クラス."""


class SecretNotFoundError(SecretStoreError):
    """シークレット未登録時のエラー."""
