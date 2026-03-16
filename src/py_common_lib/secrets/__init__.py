"""OS セキュアストレージからのシークレット取得.

仕様: docs/specs/infrastructure/secret-store.md
"""

from py_common_lib.secrets.errors import SecretNotFoundError, SecretStoreError
from py_common_lib.secrets.store import get_secret

__all__ = [
    "SecretNotFoundError",
    "SecretStoreError",
    "get_secret",
]
