"""セッション単位で切り替わるログファイルハンドラ.

仕様: docs/specs/infrastructure/session-rotating-file-handler.md
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

_SEQUENCE_WIDTH = 5


def build_session_filename(prefix: str, started_at: datetime, sequence: int) -> str:
    """セッション開始時刻と連番からログファイル名を組み立てる."""
    timestamp = started_at.strftime("%Y%m%d-%H%M%S")
    return f"{prefix}{timestamp}-{sequence:0{_SEQUENCE_WIDTH}d}.log"


class SessionRotatingFileHandler(logging.FileHandler):
    """サイズ超過時に新ファイルへ切り替える FileHandler.

    仕様: docs/specs/infrastructure/session-rotating-file-handler.md
    """

    def __init__(
        self,
        log_dir: Path,
        prefix: str,
        started_at: datetime,
        max_bytes: int,
        encoding: str = "utf-8",
    ) -> None:
        if max_bytes <= 0:
            msg = f"max_bytes must be positive, got {max_bytes}"
            raise ValueError(msg)
        self._log_dir = log_dir
        self._prefix = prefix
        self._started_at = started_at
        self._max_bytes = max_bytes
        self._sequence = 1
        self._raise_if_current_exists()
        super().__init__(self._current_path(), mode="w", encoding=encoding, delay=False)

    def _current_path(self) -> Path:
        return self._log_dir / build_session_filename(
            self._prefix, self._started_at, self._sequence
        )

    def _raise_if_current_exists(self) -> None:
        current = self._current_path()
        if current.exists():
            msg = f"Log file already exists: {current}"
            raise FileExistsError(msg)

    def emit(self, record: logging.LogRecord) -> None:
        if self.stream is None:
            self.mode = "a"
            self.stream = self._open()
        try:
            if self._should_rollover():
                self._do_rollover()
        except Exception:
            self.handleError(record)
            return
        super().emit(record)

    def _should_rollover(self) -> bool:
        if self.stream is None:
            return False
        return Path(self.baseFilename).stat().st_size >= self._max_bytes

    def _do_rollover(self) -> None:
        if self.stream is not None:
            self.stream.close()
            self.stream = None  # type: ignore[assignment]
        self._sequence += 1
        self._raise_if_current_exists()
        self.baseFilename = str(self._current_path())
        self.mode = "w"
        self.stream = self._open()
