# Contributing to Open PR Reviewer

Thanks for your interest! Contributions of all kinds are welcome — bug reports,
feature requests, documentation, and code.

## Getting started

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-change`
3. Make your changes.
4. Run the test suite: `pip install -e ".[dev]" && pytest`
5. Commit and push, then open a pull request.

## Development setup

```bash
git clone https://github.com/yourname/open-pr-reviewer.git
cd open-pr-reviewer
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## Code style

- Target Python 3.9+.
- Keep the runtime dependencies minimal (currently `requests` and `PyYAML`).
- Add tests for any new logic. Test files live in `tests/`.
- Use descriptive commit messages.

## Reporting issues

Open an issue and include:

- The exact command or workflow you ran.
- Expected vs. actual behavior.
- Relevant logs (redact any secrets).

## Code of conduct

Be respectful and constructive. Harassment of any kind will not be tolerated.