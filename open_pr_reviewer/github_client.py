"""Minimal GitHub REST client used by open-pr-reviewer.

Only depends on ``requests`` and works fine from GitHub Actions or a local
workstation with a token. All endpoints used are public GitHub REST v3.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import requests

API_BASE = "https://api.github.com"


class GitHubError(RuntimeError):
    """Raised when GitHub returns an error response."""


class GitHubClient:
    """Thin wrapper around the GitHub REST API."""

    def __init__(self, token: str, repo: Optional[str] = None, pull_number: Optional[int] = None):
        if not token:
            raise GitHubError("A GitHub token is required. Set GITHUB_TOKEN.")
        self.token = token
        self.repo = repo or os.environ.get("GITHUB_REPOSITORY", "")
        self.pull_number = pull_number
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "open-pr-reviewer/0.1.0",
            }
        )

    def _url(self, path: str) -> str:
        return f"{API_BASE}/repos/{self.repo}{path}"

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        resp = self._session.request(method, self._url(path), timeout=30, **kwargs)
        if resp.status_code >= 400:
            raise GitHubError(
                f"GitHub API error {resp.status_code} for {method} {path}: {resp.text[:500]}"
            )
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    def get_pull(self, number: int) -> Dict[str, Any]:
        """Fetch pull request metadata."""
        return self._request("GET", f"/pulls/{number}")

    def get_diff(self, number: int) -> str:
        """Fetch the unified diff for a pull request."""
        resp = self._session.get(
            f"{API_BASE}/repos/{self.repo}/pulls/{number}",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github.v3.diff",
                "User-Agent": "open-pr-reviewer/0.1.0",
            },
            timeout=60,
        )
        if resp.status_code >= 400:
            raise GitHubError(
                f"GitHub API error {resp.status_code} fetching diff: {resp.text[:500]}"
            )
        return resp.text

    def list_review_comments(self, number: int) -> List[Dict[str, Any]]:
        """List existing inline review comments (to avoid duplicates)."""
        return self._request("GET", f"/pulls/{number}/comments")

    def post_review(self, number: int, body: str, comments: List[Dict[str, Any]], event: str = "COMMENT") -> Dict[str, Any]:
        """Create a pull request review with optional inline comments."""
        payload = {
            "body": body,
            "event": event,
            "comments": comments,
        }
        return self._request("POST", f"/pulls/{number}/reviews", json=payload)

    def add_labels(self, number: int, labels: List[str]) -> None:
        """Add labels to a pull request."""
        if not labels:
            return
        self._request("POST", f"/issues/{number}/labels", json={"labels": labels})

    def get_pr_files(self, number: int) -> List[Dict[str, Any]]:
        """List files changed in a pull request."""
        return self._request("GET", f"/pulls/{number}/files")

    def create_issue_comment(self, number: int, body: str) -> Dict[str, Any]:
        """Post a plain issue comment on the pull request."""
        return self._request("POST", f"/issues/{number}/comments", json={"body": body})

    def get_authenticated_user(self) -> Dict[str, Any]:
        """Return the authenticated user (used for diagnostics)."""
        resp = self._session.get(f"{API_BASE}/user", timeout=30)
        resp.raise_for_status()
        return resp.json()