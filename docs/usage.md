# Usage Guide

This guide covers common ways to use Open PR Reviewer.

## As a GitHub Action (recommended)

Create `.github/workflows/pr-review.yml`:

```yaml
name: AI PR Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Open PR Reviewer
        uses: Lastron2000/open-pr-reviewer@v0.1.0
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
```

The action reads the pull request number from the GitHub event payload
automatically, so no extra configuration is needed.

### Advanced workflow

```yaml
- name: Run Open PR Reviewer
  uses: Lastron2000/open-pr-reviewer@v0.1.0
  with:
    openai_api_key: ${{ secrets.OPENAI_API_KEY }}
    model: gpt-4o-mini
    max_comments: "5"
    comment_threshold: "0.8"
    labels: "ai-reviewed,needs-review"
    check_for_bugs: "true"
    check_for_security: "true"
    check_for_style: "false"
    extra_instructions: |
      This project uses async/await. Flag any use of blocking I/O in async code.
```

## As a CLI

```bash
# Review PR #42 in owner/repo without posting anything
open-pr-reviewer --repo owner/repo --pull-number 42 --dry-run

# Review and write the result to a file
open-pr-reviewer --repo owner/repo --pull-number 42 --output review.json

# Use a YAML config
open-pr-reviewer --repo owner/repo --pull-number 42 --config .github/pr-review.yml
```

### Environment variables

| Variable | Required | Description |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | GitHub token with `pull-requests: write` and `issues: write`. |
| `OPENAI_API_KEY` | Yes | OpenAI API key. |
| `OPENAI_BASE_URL` | No | Override the API base URL (default `https://api.openai.com/v1`). |

## Config file reference

The YAML config file mirrors the workflow inputs:

```yaml
model: gpt-4o-mini
max_comments: 10
comment_threshold: 0.7
enabled: true
labels:
  - ai-reviewed
summarize: true
check_for_bugs: true
check_for_security: true
check_for_style: false
extra_instructions: ""
```

## Troubleshooting

**The action runs but posts nothing.**

- Confirm `OPENAI_API_KEY` is set correctly.
- Confirm the token has `pull-requests: write` permission.
- Run with `--dry-run` locally and inspect the JSON result.

**Model returns no issues.**

- Lower `comment_threshold`.
- Enable more focus areas, e.g. `check_for_style: "true"`.
- Provide more context via `extra_instructions`.

**GitHub API error 403.**

- The default `GITHUB_TOKEN` may lack permissions. Create a fine-grained PAT
  with `pull-requests: write` and `issues: write` and pass it via `github_token`.