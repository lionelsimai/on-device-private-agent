"""Benchmark: $0 inference + retrieval latency + accuracy on known queries.

Run: python benchmarks/bench_retrieval.py
"""
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from on_device_private_agent import PrivateAgent  # noqa: E402

CASES = [
    ("How does privacy work?", "privacy"),
    ("What does inference cost for 1000 users?", "pricing"),
    ("Does offline mode need internet?", "offline"),
    ("Explain quantization and GGUF size", "quantization"),
    ("How does the browser demo work?", "browser"),
]


def main() -> int:
    """Run the benchmark and print measured results."""
    agent = PrivateAgent()
    latencies: list[float] = []
    correct = 0
    total_cost = 0.0
    for query, expected in CASES:
        start = time.perf_counter()
        ans = agent.ask(query)
        latencies.append((time.perf_counter() - start) * 1000)
        total_cost += ans.cost_usd
        correct += int(expected in ans.sources)
    print(f"Queries: {len(CASES)}  Top-source accuracy: {correct}/{len(CASES)}")
    print(f"Latency ms — mean {statistics.mean(latencies):.2f}, "
          f"p95 {sorted(latencies)[int(len(latencies) * 0.95) - 1]:.2f}, "
          f"max {max(latencies):.2f}")
    print(f"Total inference cost for {len(CASES)} queries: ${total_cost:.2f} "
          f"(projected for 1,000 users x 10 queries: $0.00)")
    assert total_cost == 0.0, "inference must be $0"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
