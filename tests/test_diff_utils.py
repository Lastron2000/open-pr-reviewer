"""Tests for diff position mapping."""

from open_pr_reviewer.diff_utils import find_position, parse_hunks

SAMPLE_DIFF = """diff --git a/src/main.py b/src/main.py
index 1234567..abcdefg 100644
--- a/src/main.py
+++ b/src/main.py
@@ -10,6 +10,8 @@ def existing():
     return 1
+
+def new_function():
+    return 42
 context line
@@ -30,4 +32,5 @@ def other():
     x = 1
     x = 2
+    x = 3
     return x
"""


def test_parse_hunks():
    hunks = parse_hunks(SAMPLE_DIFF)
    assert len(hunks) == 2
    first = hunks[0]
    assert first["new_start"] == 10
    assert first["new_count"] == 8
    second = hunks[1]
    assert second["new_start"] == 32
    assert second["new_count"] == 5


def test_find_position_in_first_hunk():
    # new line 12 is the first added line in hunk 1 (offset 3)
    assert find_position(SAMPLE_DIFF, 12) == 3


def test_find_position_in_second_hunk():
    # new line 34 is the added line in hunk 2 (offset 3)
    assert find_position(SAMPLE_DIFF, 34) == 3


def test_find_position_missing_line_returns_none():
    assert find_position(SAMPLE_DIFF, 999) is None
    assert find_position(SAMPLE_DIFF, 0) is None
    assert find_position(SAMPLE_DIFF, -5) is None