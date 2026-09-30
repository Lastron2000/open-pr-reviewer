"""Core review orchestration for open-pr-reviewer."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from .diff_utils import find_position
from .github_client import GitHubClient
from .llm import chat_completion, parse_review_response
from .models import ReviewConfig
from .prompts import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)

SEVERITY_ORDER = {"critical": 0, "warning": 1, "suggestion": 2}


class ReviewResult:
    """Result of a single review run."""

    def __init__(self, summary: str = "", issues: Optional[List[Dict[str, Any]]] = None):
        self.summary = summary
        self.issues = issues or []

    def sorted_issues(self) -> List[Dict[str, Any]]:
        return sorted(
            self.issues,
            key=lambda i: SEVERITY_ORDER.get(str(i.get("severity", "suggestion")).lower(), 3),
        )

    @property
    def found_issues(self) -> bool:
        return bool(self.issues)


def review_pull_request(
    client: GitHubClient,
    config: ReviewConfig,
    pull_number: Optional[int] = None,
    api_key: Optional[str] = None,
) -> ReviewResult:
    """Run the full review pipeline for a pull request."""
    number = pull_number or client.pull_number
    if not number:
        raise ValueError("A pull request number is required.")

    logger.info("Fetching PR #%s metadata", number)
    pr = client.get_pull(number)
    logger.info("Fetching PR #%s diff", number)
    diff = client.get_diff(number)
    files = client.get_pr_files(number)

    # Existing comments, used to avoid duplicate inline comments.
    existing = client.list_review_comments(number)
    existing_bodies = {c.get("body", "").strip() for c in existing}

    if not api_key:
        from .llm import LLMError

        raise LLMError("OPENAI_API_KEY is not set.")

    logger.info("Calling model %s", config.model)
    user_prompt = build_user_prompt(pr, diff, files, config)
    raw = chat_completion(
        model=config.model,
        system=SYSTEM_PROMPT,
        user=user_prompt,
        api_key=api_key,
    )
    parsed = parse_review_response(raw)

    summary = str(parsed.get("summary", "")).strip()
    issues: List[Dict[str, Any]] = []
    for issue in parsed.get("issues", []):
        if not isinstance(issue, dict):
            continue
        message = str(issue.get("message", "")).strip()
        if not message or message in existing_bodies:
            continue
        issues.append(issue)

    result = ReviewResult(summary=summary, issues=issues)

    if issues and config.enabled:
        comments = build_inline_comments(diff, issues, config.max_comments)
        if comments:
            client.post_review(
                number=number,
                body=_review_body(result),
                comments=comments,
                event="COMMENT",
            )
            logger.info("Posted %d inline comment(s)", len(comments))
        else:
            client.create_issue_comment(number=number, body=_review_body(result))
            logger.info("Posted review summary comment")

        if config.effective_labels():
            client.add_labels(number, config.effective_labels())
            logger.info("Applied labels: %s", ",".join(config.effective_labels()))
    elif summary and config.enabled:
        client.create_issue_comment(number=number, body=summary)
        logger.info("Posted summary-only comment")

    return result


def build_inline_comments(
    diff: str,
    issues: List[Dict[str, Any]],
    max_comments: int,
) -> List[Dict[str, Any]]:
    """Convert model issues into GitHub inline review comments.

    Only issues with a valid position in the diff are included. The list is
    truncated to ``max_comments``.
    """
    comments: List[Dict[str, Any]] = []
    for issue in issues:
        if len(comments) >= max_comments:
            break
        path = str(issue.get("file", "")).strip()
        try:
            line = int(issue.get("line", 0))
        except (TypeError, ValueError):
            line = 0
        position = find_position(diff, line)
        if not position or not path:
            continue
        body = _format_issue(issue)
        comments.append(
            {
                "path": path,
                "position": position,
                "body": body,
            }
        )
    return comments


def _format_issue(issue: Dict[str, Any]) -> str:
    severity = str(issue.get("severity", "suggestion")).lower()
    message = str(issue.get("message", "")).strip()
    prefix = {
        "critical": "🔴 **Critical**",
        "warning": "🟡 **Warning**",
        "suggestion": "🔵 **Suggestion**",
    }.get(severity, "**Suggestion**")
    return f"{prefix} {message}"


def _review_body(result: ReviewResult) -> str:
    if not result.summary:
        return "## AI Review\n\nNo summary provided."
    return f"## AI Review\n\n{result.summary}"