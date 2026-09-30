"""Tests for configuration models."""

import os

from open_pr_reviewer.models import DEFAULT_CONFIG, ReviewConfig


def test_default_config():
    cfg = ReviewConfig.from_mapping(None)
    assert cfg.model == "gpt-4o-mini"
    assert cfg.max_comments == 10
    assert cfg.comment_threshold == 0.7
    assert cfg.enabled is True
    assert cfg.labels == ["ai-reviewed"]
    assert cfg.check_for_bugs is True
    assert cfg.check_for_security is True
    assert cfg.check_for_style is False


def test_custom_config():
    data = {
        "model": "gpt-4o",
        "max_comments": 3,
        "comment_threshold": 0.9,
        "enabled": False,
        "labels": ["reviewed"],
        "check_for_bugs": False,
        "check_for_security": True,
        "check_for_style": True,
        "extra_instructions": "Be nice.",
    }
    cfg = ReviewConfig.from_mapping(data)
    assert cfg.model == "gpt-4o"
    assert cfg.max_comments == 3
    assert cfg.comment_threshold == 0.9
    assert cfg.enabled is False
    assert cfg.labels == ["reviewed"]
    assert cfg.check_for_bugs is False
    assert cfg.check_for_security is True
    assert cfg.check_for_style is True
    assert cfg.extra_instructions == "Be nice."


def test_partial_config_falls_back_to_defaults():
    cfg = ReviewConfig.from_mapping({"max_comments": 5})
    assert cfg.max_comments == 5
    assert cfg.model == DEFAULT_CONFIG["model"]
    assert cfg.check_for_security is True


def test_effective_labels_override(monkeypatch):
    cfg = ReviewConfig.from_mapping(None)
    monkeypatch.setenv("INPUT_LABELS", "foo, bar")
    assert cfg.effective_labels() == ["foo", "bar"]