"""Tests for the reviewer orchestration and inline comment building."""

from open_pr_reviewer.models import ReviewConfig
from open_pr_reviewer.reviewer import _format_issue, build_inline_comments

SAMPLE_DIFF = """diff --git a/src/app.py b/src/app.py
--- a/src/app.py
+++ b/src/app.py
@@ -1,5 +1,7 @@
 def handler():
     data = request.json
+    query = "SELECT * FROM users WHERE id = " + data["id"]
+    execute(query)
     return ok()
"""


def test_build_inline_comments_maps_positions():
    issues = [
        {
            "severity": "critical",
            "file": "src/app.py",
            "line": 3,
            "message": "SQL injection risk.",
        }
    ]
    comments = build_inline_comments(SAMPLE_DIFF, issues, max_comments=10)
    assert len(comments) == 1
    assert comments[0]["path"] == "src/app.py"
    assert comments[0]["position"] == 3
    assert "SQL injection" in comments[0]["body"]


def test_build_inline_comments_skips_missing_position():
    issues = [
        {"severity": "warning", "file": "src/app.py", "line": 999, "message": "nope"}
    ]
    comments = build_inline_comments(SAMPLE_DIFF, issues, max_comments=10)
    assert comments == []


def test_build_inline_comments_respects_max():
    issues = [
        {"severity": "warning", "file": "src/app.py", "line": 3, "message": f"issue {i}"}
        for i in range(5)
    ]
    comments = build_inline_comments(SAMPLE_DIFF, issues, max_comments=2)
    assert len(comments) == 2


def test_format_issue_severity_prefix():
    assert "Critical" in _format_issue({"severity": "critical", "message": "boom"})
    assert "Warning" in _format_issue({"severity": "warning", "message": "careful"})
    assert "Suggestion" in _format_issue({"severity": "suggestion", "message": "maybe"})