"""Environment-based configuration. No secrets are hardcoded.

Every setting has a safe offline default; override via environment variables
prefixed ``PRIVATE_AGENT_``.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


class PrivateAgentError(RuntimeError):
    """Structured error raised for invalid configuration or usage."""


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from the environment."""

    data_dir: str = "data"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> Settings:
        """Build settings from ``PRIVATE_AGENT_*`` environment variables."""
        return cls(
            data_dir=os.environ.get("PRIVATE_AGENT_DATA_DIR", "data"),
            log_level=os.environ.get("PRIVATE_AGENT_LOG_LEVEL", "INFO"),
        )
