"""End-to-end test of the review pipeline with a mocked GitHub client."""

from unittest.mock import MagicMock

from open_pr_reviewer.github_client import GitHubClient
from open_pr_reviewer.models import ReviewConfig
from open_pr_reviewer.reviewer import review_pull_request

MOCK_DIFF = """diff --git a/src/app.py b/src/app.py
--- a/src/app.py
+++ b/src/app.py
@@ -1,5 +1,7 @@
 def handler():
     data = request.json
+    query = "SELECT * FROM users WHERE id = " + data["id"]
+    execute(query)
     return ok()
"""

MOCK_PR = {
    "number": 42,
    "title": "Add user lookup endpoint",
    "body": "Implements GET /users/:id",
    "base": {"repo": {"full_name": "owner/repo"}},
}

MOCK_FILES = [
    {"filename": "src/app.py", "additions": 2, "deletions": 0},
]

MODEL_RESPONSE = """{
  "summary": "Adds a user lookup endpoint. The SQL query is built by string concatenation, which is unsafe.",
  "issues": [
    {
      "severity": "critical",
      "file": "src/app.py",
      "line": 3,
      "message": "SQL injection risk: user input is interpolated into a query."
    }
  ]
}"""


def test_end_to_end_posts_review_and_labels(monkeypatch):
    client = MagicMock(spec=GitHubClient)
    client.pull_number = 42
    client.get_pull.return_value = MOCK_PR
    client.get_diff.return_value = MOCK_DIFF
    client.get_pr_files.return_value = MOCK_FILES
    client.list_review_comments.return_value = []
    client.post_review.return_value = {"id": 1}
    client.create_issue_comment.return_value = {"id": 1}
    client.add_labels.return_value = None

    import open_pr_reviewer.reviewer as reviewer

    monkeypatch.setattr(reviewer, "chat_completion", lambda **kw: MODEL_RESPONSE)

    config = ReviewConfig.from_mapping(None)
    result = review_pull_request(
        client=client,
        config=config,
        pull_number=42,
        api_key="sk-test",
    )

    assert result.found_issues is True
    assert len(result.issues) == 1
    assert result.issues[0]["severity"] == "critical"

    client.post_review.assert_called_once()
    _, kwargs = client.post_review.call_args
    assert kwargs["number"] == 42
    assert kwargs["comments"][0]["path"] == "src/app.py"
    assert kwargs["comments"][0]["position"] == 3
    assert "SQL injection" in kwargs["comments"][0]["body"]

    client.add_labels.assert_called_once_with(42, ["ai-reviewed"])