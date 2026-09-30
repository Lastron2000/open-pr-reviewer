"""Tests for LLM response parsing."""

import pytest

from open_pr_reviewer.llm import LLMError, parse_review_response


def test_parse_plain_json():
    raw = '{"summary": "Looks good.", "issues": []}'
    data = parse_review_response(raw)
    assert data["summary"] == "Looks good."
    assert data["issues"] == []


def test_parse_fenced_json():
    raw = '''```json
{"summary": "ok", "issues": [{"severity": "warning", "file": "a.py", "line": 1, "message": "x"}]}
```'''
    data = parse_review_response(raw)
    assert data["summary"] == "ok"
    assert len(data["issues"]) == 1


def test_parse_json_embedded_in_text():
    raw = 'Sure! Here you go:\n{"summary": "s", "issues": []}\nHope that helps.'
    data = parse_review_response(raw)
    assert data["summary"] == "s"


def test_parse_invalid_raises():
    with pytest.raises(LLMError):
        parse_review_response("not json at all")


def test_defaults():
    data = parse_review_response("{}")
    assert data["summary"] == ""
    assert data["issues"] == []