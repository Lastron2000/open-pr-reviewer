<div align="center">

# 🔍 Open PR Reviewer

**Free, open-source AI pull request review powered by OpenAI.**

Automatically reviews every pull request in your repository — catches bugs, security
issues, and API misuse — then posts inline comments and a summary. Self-hosted in
GitHub Actions, no paid service required.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](pyproject.toml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

---

## Why Open PR Reviewer?

Most AI code-review tools are closed-source SaaS with per-seat pricing and send your
code to a third-party server. Open PR Reviewer is different:

- **100% open source** — MIT licensed, everything runs in your own repository.
- **Your code stays in GitHub** — the diff goes directly to OpenAI; no middleman.
- **Free to self-host** — uses standard GitHub Actions and your own OpenAI API key.
- **Configurable** — pick the model, review focus, comment volume, and labels.
- **Composable** — use it as a GitHub Action, a CLI, or a library in your own tooling.

## Why I built this

I maintain small open-source projects in my spare time, and I kept running into the
same problem: I'd open a PR, and then nothing would happen. Months later I'd dig
through my own history and realize nobody ever reviewed it. The code just got merged.

It's not that I don't care about review. It's that open source built on evenings and
weekends leaves no bandwidth to sit and read other people's diffs. The tools that
do exist are either priced per seat, or they ship your code to a third-party
server — neither of which works for a small project, and the second one I just
wasn't comfortable with.

So the goal here is narrow: make "open a PR, get a review in ten minutes" the
default behavior instead of the exception.

**This project is early.** 0 stars, 18 passing tests, and no real production
battle-testing yet. If you try it and it breaks, that's genuinely useful
information to me — please open an issue.

## Features

- ✅ **Inline code review** — comments are anchored to the exact diff lines.
- ✅ **Severity levels** — each comment is tagged `critical`, `warning`, or `suggestion`.
- ✅ **PR summary** — a high-level overview of the change and its health.
- ✅ **Duplicate avoidance** — skips issues already raised by previous runs.
- ✅ **Labeling** — automatically applies a configurable label to reviewed PRs.
- ✅ **Dry-run mode** — inspect what the model would say before posting anything.
- ✅ **Flexible models** — works with any OpenAI-compatible chat completions endpoint.

## Quick Start

### 1. Add the workflow file

Create `.github/workflows/pr-review.yml` in your repository:

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
          github_token: ${{ secrets.GITHUB_TOKEN }}
          model: gpt-4o-mini
```

### 2. Add your OpenAI API key

Go to **Settings → Secrets and variables → Actions** and add a repository secret
named `OPENAI_API_KEY` with your key from [platform.openai.com](https://platform.openai.com/api-keys).

### 3. Open a pull request

That's it. Every new PR (and every push to an open PR) is reviewed automatically.

## Configuration

You can configure the action entirely through workflow inputs, or with a YAML file
committed to your repository.

### Workflow inputs

| Input | Default | Description |
| --- | --- | --- |
| `openai_api_key` | *(required)* | OpenAI API key. |
| `github_token` | `${{ github.token }}` | Token used to post reviews. |
| `model` | `gpt-4o-mini` | OpenAI model for the review. |
| `max_comments` | `10` | Maximum inline comments per PR. |
| `comment_threshold` | `0.7` | Minimum confidence (0–1) to report an issue. |
| `labels` | `ai-reviewed` | Comma-separated labels to apply. |
| `check_for_bugs` | `true` | Review for correctness bugs. |
| `check_for_security` | `true` | Review for security vulnerabilities. |
| `check_for_style` | `false` | Review for style and maintainability. |
| `extra_instructions` | *(empty)* | Extra guidance appended to the prompt. |
| `config_path` | *(empty)* | Path to a YAML config file. |

### YAML config file

Commit a file (e.g. `.github/pr-review.yml`) and pass `config_path`:

```yaml
model: gpt-4o-mini
max_comments: 10
comment_threshold: 0.7
enabled: true
labels:
  - ai-reviewed
check_for_bugs: true
check_for_security: true
check_for_style: false
extra_instructions: >
  Prefer concrete, actionable feedback. Reference function names and line
  numbers. Do not request changes for subjective preferences.
```

See [`examples/pr-review.yml`](examples/pr-review.yml) for a full example.

## CLI usage

You can also run the reviewer locally on any PR:

```bash
export GITHUB_TOKEN=ghp_xxx
export OPENAI_API_KEY=sk-xxx

open-pr-reviewer --repo owner/repo --pull-number 123 --dry-run
open-pr-reviewer --repo owner/repo --pull-number 123 --output review.json
```

Flags:

- `--repo owner/name` — repository to review (defaults to `GITHUB_REPOSITORY`).
- `--pull-number N` — pull request number.
- `--config path` — YAML config file.
- `--dry-run` — analyze but do not post anything.
- `--output path` — write the result as JSON.
- `--verbose` — debug logging.

## How it works

1. A GitHub Actions workflow triggers on `pull_request`.
2. `open-pr-reviewer` fetches the PR metadata, changed files, and unified diff.
3. The diff is sent to OpenAI with a structured review prompt.
4. The model returns a JSON object with a summary and a list of issues.
5. The action posts an inline review with comments anchored to diff positions,
   and applies a configurable label.

```
pull_request → checkout → open-pr-reviewer → GitHub API → OpenAI → inline review
                     └────────── diff ──────────┘        └── JSON ──→ comments
```

## Development

```bash
git clone https://github.com/Lastron2000/open-pr-reviewer.git
cd open-pr-reviewer
pip install -e ".[dev]"
pytest
```

## License

[MIT](LICENSE)

## Contributing

Contributions are welcome. Open an issue or submit a pull request. See
[CONTRIBUTING.md](CONTRIBUTING.md).