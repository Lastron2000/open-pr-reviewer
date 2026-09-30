"""Utilities for mapping model-reported line numbers onto diff hunks.

GitHub inline review comments require ``position`` (a 1-based index within the
diff hunk). This module converts an absolute new-file line number into a diff
position by walking the unified diff hunks.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

HUNK_HEADER = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")

# Inline comment positions have a hard API limit.
MAX_POSITION = 100_000


def parse_hunks(diff: str) -> List[Dict[str, int]]:
    """Parse a unified diff into a list of hunk metadata.

    Each hunk dict has keys: old_start, old_count, new_start, new_count,
    and a list of new-file line numbers in order.
    """
    hunks: List[Dict[str, int]] = []
    current: Optional[Dict[str, int]] = None
    new_line: Optional[int] = None

    for raw_line in diff.splitlines():
        if raw_line.startswith("+++") or raw_line.startswith("---"):
            continue
        match = HUNK_HEADER.match(raw_line)
        if match:
            if current:
                hunks.append(current)
            old_start = int(match.group(1))
            old_count = int(match.group(2) or 1)
            new_start = int(match.group(3))
            new_count = int(match.group(4) or 1)
            current = {
                "old_start": old_start,
                "old_count": old_count,
                "new_start": new_start,
                "new_count": new_count,
            }
            new_line = new_start
            continue
        if current is None:
            continue
        if raw_line.startswith("+"):
            current[new_line] = new_line  # type: ignore[assignment]
            new_line += 1
        elif raw_line.startswith("-"):
            continue
        elif raw_line.startswith("\\"):
            continue
        else:
            new_line += 1

    if current:
        hunks.append(current)
    return hunks


def find_position(diff: str, target_line: int) -> Optional[int]:
    """Return the diff position for a target new-file line, or None."""
    if target_line <= 0:
        return None
    for hunk in parse_hunks(diff):
        new_start = hunk["new_start"]
        new_count = hunk["new_count"]
        if new_start <= target_line < new_start + new_count:
            position = target_line - new_start + 1
            if 1 <= position <= MAX_POSITION:
                return position
    return None