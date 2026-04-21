"""セッション単位ログファイルハンドラのテスト.

仕様: docs/specs/infrastructure/session-rotating-file-handler.md
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import pytest

from py_common_lib.logging import (
    SessionRotatingFileHandler,
    build_session_filename,
)

_PREFIX = "app-server-"


def _make_record(message: str) -> logging.LogRecord:
    return logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg=message,
        args=(),
        exc_info=None,
    )


class TestBuildSessionFilename:
    def test_format_uses_prefix_timestamp_and_zero_padded_sequence(self) -> None:
        started_at = datetime(2026, 4, 17, 8, 30, 0)
        assert (
            build_session_filename(_PREFIX, started_at, 1) == "app-server-20260417-083000-00001.log"
        )

    def test_sequence_increments_preserve_five_digit_padding(self) -> None:
        started_at = datetime(2026, 4, 17, 8, 30, 0)
        assert (
            build_session_filename(_PREFIX, started_at, 42)
            == "app-server-20260417-083000-00042.log"
        )

    def test_different_prefix_produces_different_filename(self) -> None:
        started_at = datetime(2026, 4, 17, 8, 30, 0)
        assert (
            build_session_filename("rag-server-", started_at, 1)
            == "rag-server-20260417-083000-00001.log"
        )


class TestSessionRotatingFileHandler:
    def test_initial_file_is_created_with_sequence_one(self, tmp_path: Path) -> None:
        started_at = datetime(2026, 4, 17, 8, 30, 0)
        handler = SessionRotatingFileHandler(
            log_dir=tmp_path, prefix=_PREFIX, started_at=started_at, max_bytes=1_000_000
        )
        try:
            handler.emit(_make_record("hello"))
            handler.flush()
        finally:
            handler.close()
        expected = tmp_path / "app-server-20260417-083000-00001.log"
        assert expected.exists()
        assert "hello" in expected.read_text(encoding="utf-8")

    def test_rollover_opens_new_file_while_keeping_previous(self, tmp_path: Path) -> None:
        started_at = datetime(2026, 4, 17, 8, 30, 0)
        handler = SessionRotatingFileHandler(
            log_dir=tmp_path, prefix=_PREFIX, started_at=started_at, max_bytes=50
        )
        try:
            handler.emit(_make_record("seed-line" + "x" * 40))
            for i in range(10):
                handler.emit(_make_record(f"line-{i:02d}" + "x" * 40))
            handler.flush()
        finally:
            handler.close()
        first = tmp_path / "app-server-20260417-083000-00001.log"
        second = tmp_path / "app-server-20260417-083000-00002.log"
        assert first.exists()
        assert second.exists()
        first_content = first.read_text(encoding="utf-8")
        assert "seed-line" in first_content
        assert second.stat().st_size > 0

    def test_existing_initial_file_raises_file_exists_error(self, tmp_path: Path) -> None:
        started_at = datetime(2026, 4, 17, 8, 30, 0)
        conflicting = tmp_path / "app-server-20260417-083000-00001.log"
        conflicting.write_text("preexisting", encoding="utf-8")
        with pytest.raises(FileExistsError):
            SessionRotatingFileHandler(
                log_dir=tmp_path,
                prefix=_PREFIX,
                started_at=started_at,
                max_bytes=1_000_000,
            )

    @pytest.mark.parametrize("invalid_value", [0, -1])
    def test_zero_or_negative_max_bytes_raises_value_error(
        self, tmp_path: Path, invalid_value: int
    ) -> None:
        with pytest.raises(ValueError, match="max_bytes must be positive"):
            SessionRotatingFileHandler(
                log_dir=tmp_path,
                prefix=_PREFIX,
                started_at=datetime(2026, 4, 17, 8, 30, 0),
                max_bytes=invalid_value,
            )

    def test_rollover_raises_when_next_file_already_exists(self, tmp_path: Path) -> None:
        """ロールオーバー先ファイルが既存の場合、emit 経由で handleError に委ねる."""
        started_at = datetime(2026, 4, 17, 8, 30, 0)
        conflicting = tmp_path / "app-server-20260417-083000-00002.log"
        conflicting.write_text("preexisting", encoding="utf-8")
        handler = SessionRotatingFileHandler(
            log_dir=tmp_path, prefix=_PREFIX, started_at=started_at, max_bytes=50
        )
        errors: list[BaseException] = []
        handler.handleError = (  # type: ignore[method-assign]
            lambda record: errors.append(  # noqa: ARG005
                FileExistsError("rollover collision")
            )
        )
        try:
            for i in range(10):
                handler.emit(_make_record(f"line-{i}" + "x" * 40))
        finally:
            handler.close()
        assert errors, "handleError should capture rollover FileExistsError"
        assert conflicting.read_text(encoding="utf-8") == "preexisting"

    def test_emit_reopens_stream_in_append_mode(self, tmp_path: Path) -> None:
        """stream=None 状態で emit されると mode='a' で再オープンされ既存内容を保持する."""
        started_at = datetime(2026, 4, 17, 8, 30, 0)
        handler = SessionRotatingFileHandler(
            log_dir=tmp_path, prefix=_PREFIX, started_at=started_at, max_bytes=1_000_000
        )
        handler.emit(_make_record("first"))
        handler.flush()
        assert handler.stream is not None
        handler.stream.close()
        handler.stream = None  # type: ignore[assignment]

        try:
            handler.emit(_make_record("second"))
            handler.flush()
        finally:
            handler.close()

        assert handler.mode == "a"
        log_path = tmp_path / "app-server-20260417-083000-00001.log"
        content = log_path.read_text(encoding="utf-8")
        assert "first" in content
        assert "second" in content
