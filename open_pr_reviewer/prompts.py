"""Prompt construction for the OpenAI review call."""

from __future__ import annotations

from typing import Any, Dict, List

from .models import ReviewConfig

SYSTEM_PROMPT = """You are a senior software engineer performing a thorough pull request review.
Focus on issues that genuinely matter: correctness bugs, security problems, concurrency and
performance issues, and API misuse. Ignore trivial style nits unless explicitly asked.

For each issue, provide:
1. severity: one of "critical", "warning", "suggestion"
2. file: path of the affected file
3. line: the relevant line number (1-based) or 0 if unknown
4. message: a concise, specific, actionable explanation

Only report issues you are confident about. If there is nothing worth reporting, return an empty list."""

EXAMPLE_OUTPUT = """{
  "summary": "A one-paragraph overview of the change and overall health.",
  "issues": [
    {
      "severity": "critical",
      "file": "src/main.py",
      "line": 42,
      "message": "Potential SQL injection: f-string interpolation into a query. Use parameterized queries."
    }
  ]
}"""


def _file_context(files: List[Dict[str, Any]], diff: str, config: ReviewConfig) -> str:
    """Build the file list portion of the user prompt."""
    if not files:
        return "No file list was provided. Use the diff below."
    lines = ["Changed files:"]
    for f in files:
        additions = f.get("additions", 0)
        deletions = f.get("deletions", 0)
        lines.append(f"- {f.get('filename', '?')} (+{additions}/-{deletions})")
    return "\n".join(lines)


def build_user_prompt(
    pr: Dict[str, Any],
    diff: str,
    files: List[Dict[str, Any]],
    config: ReviewConfig,
) -> str:
    """Assemble the user prompt sent to the model."""
    checks = []
    if config.check_for_bugs:
        checks.append("correctness bugs and logic errors")
    if config.check_for_security:
        checks.append("security vulnerabilities")
    if config.check_for_style:
        checks.append("style and maintainability problems")
    if not checks:
        checks = ["correctness bugs and logic errors"]

    instructions = (
        "\n\nAdditional reviewer instructions:\n" + config.extra_instructions
        if config.extra_instructions
        else ""
    )

    return f"""You are reviewing GitHub pull request #{pr.get('number')} in {pr.get('base', {}).get('repo', {}).get('full_name', 'the repository')}.

Title: {pr.get('title', '')}
Description:
{pr.get('body') or '(no description provided)'}

Focus areas: {', '.join(checks)}.
Report at most {config.max_comments} issues, ordered by severity.
Only include issues with confidence at least {config.comment_threshold}.
{instructions}

{_file_context(files, diff, config)}

Here is the unified diff:

```diff
{diff}
```

Respond with strict JSON only:
{EXAMPLE_OUTPUT}"""