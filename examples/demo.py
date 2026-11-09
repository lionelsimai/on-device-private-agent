"""Run: python examples/demo.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from on_device_private_agent import PrivateAgent

if __name__ == "__main__":
    agent = PrivateAgent()
    for q in ["How does privacy work?", "summarise offline mode"]:
        a = agent.ask(q)
        print(q, "->", a.text, "| sources:", a.sources, "| cost:", a.cost_usd)
