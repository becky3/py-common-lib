"""httpx 用の制約付き HTTP クライアント."""

from py_common_lib.httpx.constrained_client import (
    ConstrainedClient,
    clamp_operation_timeout,
    clamp_request_interval,
    clamp_request_timeout,
)

__all__ = [
    "ConstrainedClient",
    "clamp_operation_timeout",
    "clamp_request_interval",
    "clamp_request_timeout",
]
