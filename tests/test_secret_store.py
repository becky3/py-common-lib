"""シークレットストアのテスト.

テスト方針:
- keyring はモックで差し替え、OS セキュアストレージには依存しない
- 仕様書のインターフェース定義・エッジケースを網羅する
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from keyring.errors import KeyringError

from py_common_lib.secrets import SecretNotFoundError, SecretStoreError, get_secret


class TestGetSecret:
    """get_secret のテスト."""

    def test_returns_registered_value(self) -> None:
        """登録済みのシークレットを正常に取得できる."""
        with patch("py_common_lib.secrets.store.keyring.get_password", return_value="secret-value"):
            result = get_secret("API_KEY", service="test-service")
        assert result == "secret-value"

    def test_raises_not_found_for_unregistered_key(self) -> None:
        """未登録のキーで SecretNotFoundError を送出する."""
        with patch("py_common_lib.secrets.store.keyring.get_password", return_value=None):
            with pytest.raises(SecretNotFoundError, match="test-service.*UNKNOWN_KEY"):
                get_secret("UNKNOWN_KEY", service="test-service")

    def test_error_message_contains_service_and_key(self) -> None:
        """エラーメッセージにサービス名とキー名が含まれる."""
        with patch("py_common_lib.secrets.store.keyring.get_password", return_value=None):
            with pytest.raises(SecretNotFoundError) as exc_info:
                get_secret("MY_KEY", service="my-service")
        assert "my-service" in str(exc_info.value)
        assert "MY_KEY" in str(exc_info.value)

    def test_returns_empty_string_when_registered(self) -> None:
        """空文字列が登録されている場合は正常に返す（未登録とは区別）."""
        with patch("py_common_lib.secrets.store.keyring.get_password", return_value=""):
            result = get_secret("EMPTY_KEY", service="test-service")
        assert result == ""

    def test_raises_store_error_on_backend_failure(self) -> None:
        """バックエンドアクセス失敗時に SecretStoreError を送出する."""
        with patch(
            "py_common_lib.secrets.store.keyring.get_password",
            side_effect=KeyringError("backend unavailable"),
        ):
            with pytest.raises(SecretStoreError, match="Failed to access secret store"):
                get_secret("API_KEY", service="test-service")

    def test_store_error_chains_original_exception(self) -> None:
        """SecretStoreError が元の例外をチェーンする."""
        original = KeyringError("backend error")
        with patch(
            "py_common_lib.secrets.store.keyring.get_password",
            side_effect=original,
        ):
            with pytest.raises(SecretStoreError) as exc_info:
                get_secret("API_KEY", service="test-service")
        assert exc_info.value.__cause__ is original


class TestErrorHierarchy:
    """エラー型の階層テスト."""

    def test_not_found_is_subclass_of_store_error(self) -> None:
        """SecretNotFoundError は SecretStoreError のサブクラス."""
        assert issubclass(SecretNotFoundError, SecretStoreError)

    def test_store_error_is_subclass_of_exception(self) -> None:
        """SecretStoreError は Exception のサブクラス."""
        assert issubclass(SecretStoreError, Exception)
