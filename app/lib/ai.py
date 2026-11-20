"""One `ask()` for every AI feature, with three interchangeable backends.

Backend is chosen by AI_PROVIDER in .env:
  - "claude"  : Anthropic API (needs ANTHROPIC_API_KEY)
  - "granite" : IBM Granite running locally in Ollama (http://localhost:11434), no key needed
  - "offline" : no model; returns a deterministic summary so a live demo never breaks
If the chosen backend fails, ask() falls back to "offline" and says so, instead of crashing.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

load_dotenv()

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-5-5")
GRANITE_MODEL = os.getenv("GRANITE_MODEL", "granite3.3:8b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")


@dataclass
class Answer:
    text: str
    backend: str
    note: str = ""


def provider() -> str:
    p = os.getenv("AI_PROVIDER", "").strip().lower()
    if p:
        return p
    return "claude" if os.getenv("ANTHROPIC_API_KEY") else "offline"


def _claude(system: str, messages: list[dict]) -> str:
    import anthropic

    client = anthropic.Anthropic()
    resp = client.beta.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=16000,
        system=system,
        messages=messages,
        output_config={"effort": "low"},          # chat-style answers: fast and cheap
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",                       # reroute policy declines automatically
    )
    if resp.stop_reason == "refusal":
        return "The model declined this request. Try rephrasing it."
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def _granite(system: str, messages: list[dict]) -> str:
    r = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": GRANITE_MODEL, "stream": False,
              "messages": [{"role": "system", "content": system}, *messages]},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["message"]["content"].strip()


def _offline(system: str, messages: list[dict]) -> str:
    last = messages[-1]["content"] if messages else ""
    return (
        "**Offline mode** (no AI backend configured). Your question was recorded:\n\n"
        f"> {last[:400]}\n\n"
        "Set `AI_PROVIDER` and a key in `.env` to get generated answers."
    )


BACKENDS = {"claude": _claude, "granite": _granite, "offline": _offline}


def ask(prompt: str, system: str = "You are a concise, accurate assistant.",
        history: list[dict] | None = None) -> Answer:
    messages = [*(history or []), {"role": "user", "content": prompt}]
    name = provider()
    fn = BACKENDS.get(name, _offline)
    try:
        return Answer(fn(system, messages), name)
    except Exception as exc:  # demo safety: never crash the UI on an AI failure
        return Answer(_offline(system, messages), "offline", f"{name} failed: {type(exc).__name__}: {exc}")
