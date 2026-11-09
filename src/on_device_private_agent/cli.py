"""CLI: ``private-agent demo`` and ``private-agent ask "..."``."""
from __future__ import annotations

import argparse
import json

from .core import PrivateAgent


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    ap = argparse.ArgumentParser(prog="private-agent")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    ask_parser = sub.add_parser("ask")
    ask_parser.add_argument("query")
    args = ap.parse_args(argv)
    agent = PrivateAgent()
    if args.cmd == "ask":
        ans = agent.ask(args.query)
        print(json.dumps({"text": ans.text, "intent": ans.intent,
                          "sources": ans.sources, "cost_usd": ans.cost_usd}, indent=2))
        return 0
    # demo
    for q in ["How does privacy work?",
              "What does inference cost for 1000 users?",
              "summarise quantization"]:
        ans = agent.ask(q)
        print(f"Q: {q}\nA: {ans.text}\n  sources={ans.sources} cost=${ans.cost_usd}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
