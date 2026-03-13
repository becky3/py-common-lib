"""パッケージのインポートテスト."""

import py_common_lib
import py_common_lib.core
import py_common_lib.httpx


def test_package_import() -> None:
    """パッケージがインポートできることを確認する."""
    assert py_common_lib.__name__ == "py_common_lib"
    assert py_common_lib.core.__name__ == "py_common_lib.core"
    assert py_common_lib.httpx.__name__ == "py_common_lib.httpx"
