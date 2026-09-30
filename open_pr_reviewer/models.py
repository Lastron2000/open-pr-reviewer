"""Configuration models for open-pr-reviewer."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

DEFAULT_CONFIG = {
    "model": "gpt-4o-mini",
    "max_comments": 10,
    "comment_threshold": 0.7,
    "enabled": True,
    "labels": ["ai-reviewed"],
    "summarize": True,
    "check_for_bugs": True,
    "check_for_security": True,
    "check_for_style": False,
    "extra_instructions": "",
}


def _env_or_default(key: str, default: str) -> str:
    return os.environ.get(key, default)


@dataclass
class ReviewConfig:
    """Resolved configuration for a single review run."""

    model: str = "gpt-4o-mini"
    max_comments: int = 10
    comment_threshold: float = 0.7
    enabled: bool = True
    labels: List[str] = field(default_factory=lambda: ["ai-reviewed"])
    summarize: bool = True
    check_for_bugs: bool = True
    check_for_security: bool = True
    check_for_style: bool = False
    extra_instructions: str = ""

    @classmethod
    def from_mapping(cls, data: Optional[Dict[str, Any]]) -> "ReviewConfig":
        """Build a config from a nested mapping, falling back to defaults."""
        merged: Dict[str, Any] = dict(DEFAULT_CONFIG)
        if data:
            for key in DEFAULT_CONFIG:
                if key in data:
                    merged[key] = data[key]
        return cls(
            model=str(merged["model"]),
            max_comments=int(merged["max_comments"]),
            comment_threshold=float(merged["comment_threshold"]),
            enabled=bool(merged["enabled"]),
            labels=[str(x) for x in merged.get("labels", [])],
            summarize=bool(merged["summarize"]),
            check_for_bugs=bool(merged["check_for_bugs"]),
            check_for_security=bool(merged["check_for_security"]),
            check_for_style=bool(merged["check_for_style"]),
            extra_instructions=str(merged.get("extra_instructions", "")),
        )

    def effective_labels(self) -> List[str]:
        """Return labels to apply, honoring an optional override env var."""
        override = os.environ.get("INPUT_LABELS", "").strip()
        if override:
            return [x.strip() for x in override.split(",") if x.strip()]
        return self.labels