"""Rule-based planner: maps a query to an intent + action without an LLM."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Plan:
    """A planned action for a query."""

    intent: str
    action: str  # retrieve | summarise | list | help
    query: str


_RULES: list[tuple[str, str, tuple[str, ...]]] = [
    ("summarise", "summarise", ("summarise", "summarize", "summary", "tldr")),
    ("list", "list", ("list", "show all", "what documents", "what docs")),
    ("help", "help", ("help", "what can you", "how do you work")),
]


def plan(query: str) -> Plan:
    """Return the Plan for ``query`` (default: retrieve)."""
    q = query.lower().strip()
    for intent, action, keys in _RULES:
        if any(k in q for k in keys):
            return Plan(intent=intent, action=action, query=query)
    return Plan(intent="question", action="retrieve", query=query)
