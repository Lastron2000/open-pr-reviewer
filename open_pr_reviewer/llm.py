"""OpenAI chat completions client used by open-pr-reviewer.

Uses the public ``/v1/chat/completions`` endpoint so it works with the OpenAI
API, Azure OpenAI, or any compatible gateway by setting ``OPENAI_BASE_URL``.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import requests


class LLMError(RuntimeError):
    """Raised when the model call fails."""


def _base_url() -> str:
    return os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")


def chat_completion(
    model: str,
    system: str,
    user: str,
    api_key: str,
    max_tokens: int = 4000,
    temperature: float = 0.2,
) -> str:
    """Call the chat completions API and return the assistant message text."""
    if not api_key:
        raise LLMError("OPENAI_API_KEY is not set.")

    url = f"{_base_url()}/chat/completions"
    payload: Dict[str, Any] = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=120)
    if resp.status_code >= 400:
        raise LLMError(
            f"OpenAI API error {resp.status_code}: {resp.text[:500]}"
        )
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def parse_review_response(raw: str) -> Dict[str, Any]:
    """Parse the model response into a dict with a summary and issues list.

    Tolerates markdown code fences and a small amount of surrounding text.
    """
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Fall back to extracting the first {...} block.
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise LLMError("Model response was not valid JSON.")
        try:
            data = json.loads(text[start : end + 1])
        except json.JSONDecodeError as exc:
            raise LLMError(f"Could not parse model response as JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise LLMError("Model response JSON was not an object.")
    data.setdefault("summary", "")
    data.setdefault("issues", [])
    return data