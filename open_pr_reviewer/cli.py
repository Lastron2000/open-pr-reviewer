"""Command-line entry point for open-pr-reviewer."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from typing import Optional

import yaml

from . import __version__
from .github_client import GitHubClient
from .llm import LLMError
from .models import ReviewConfig
from .reviewer import review_pull_request


def _load_config(path: Optional[str]):
    """Load config from a YAML file, or return None for defaults."""
    if not path:
        return None
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="open-pr-reviewer",
        description="Open-source AI pull request reviewer.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--pull-number", type=int, help="Pull request number to review.")
    parser.add_argument(
        "--repo",
        help="Repository in owner/name form. Defaults to GITHUB_REPOSITORY.",
    )
    parser.add_argument("--config", help="Path to a YAML config file.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and analyze the PR but do not post anything.",
    )
    parser.add_argument(
        "--output",
        help="Write the review result to a JSON file (also printed to stdout).",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging."
    )
    return parser.parse_args(argv)


def main(argv: Optional[list] = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)

    token = os.environ.get("GITHUB_TOKEN", "")
    api_key = os.environ.get("OPENAI_API_KEY", "")

    config_data = _load_config(args.config)
    config = ReviewConfig.from_mapping(config_data)
    if args.dry_run:
        config.enabled = False

    try:
        client = GitHubClient(token=token, repo=args.repo)
        result = review_pull_request(
            client=client,
            config=config,
            pull_number=args.pull_number,
            api_key=api_key,
        )
    except (GitHubClient, LLMError, ValueError, FileNotFoundError) as exc:  # noqa: F821
        logger.error("%s", exc)
        return 1

    payload = {
        "summary": result.summary,
        "issues": result.issues,
        "found_issues": result.found_issues,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        logger.info("Wrote result to %s", args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())