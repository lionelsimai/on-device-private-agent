"""Benchmark: local inference cost + retrieval latency + accuracy.

24 hand-written queries (4-5 per document). Latency reports mean, p95
(nearest-rank over the 24 samples) and max. Cost is *measured*: the agent
makes no API calls, so the marginal cost per query is local CPU time only.

Run: python benchmarks/bench_retrieval.py
"""
import math
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from on_device_private_agent import PrivateAgent  # noqa: E402

CASES = [
    ("How does privacy work?", "privacy"),
    ("Does my query leave the device?", "privacy"),
    ("Is an API key required?", "privacy"),
    ("Are documents indexed locally with TF-IDF?", "privacy"),
    ("No query leaves the device — is that the privacy model?", "privacy"),
    ("What does inference cost for 1000 users?", "pricing"),
    ("How much does inference cost in dollars?", "pricing"),
    ("What is the inference cost per user?", "pricing"),
    ("Why does inference cost zero dollars?", "pricing"),
    ("What is the total inference bill for a thousand users?", "pricing"),
    ("Does offline mode need internet?", "offline"),
    ("Can I use offline mode without internet?", "offline"),
    ("Does the offline fallback run locally?", "offline"),
    ("What can be cached by service workers for offline use?", "offline"),
    ("Does offline mode work without internet?", "offline"),
    ("Explain quantization and GGUF size", "quantization"),
    ("How much smaller is a Q4 GGUF model than FP16?", "quantization"),
    ("Does quantization reduce model size and memory use?", "quantization"),
    ("What does the quantization guide say about quality drop?", "quantization"),
    ("How much memory does a Q4 model use?", "quantization"),
    ("How does the browser demo work?", "browser"),
    ("Does the browser demo need a download?", "browser"),
    ("What runs in the browser when WebGPU is available?", "browser"),
    ("Is the WebLLM hook a stub?", "browser"),
]


def _p95(samples: list[float]) -> float:
    """Nearest-rank p95 (valid for the 24-sample run)."""
    ordered = sorted(samples)
    return ordered[math.ceil(0.95 * len(ordered)) - 1]


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
    n = len(CASES)
    print(f"Queries: {n}  Top-source accuracy (expected in used sources): "
          f"{correct}/{n}")
    print(f"Latency ms — mean {statistics.mean(latencies):.2f}, "
          f"p95 {_p95(latencies):.2f}, max {max(latencies):.2f}")
    projected = total_cost * (10_000 / n)
    print(f"Measured inference cost for {n} queries: ${total_cost:.2f}")
    print(f"Projected cost for 1,000 users x 10 queries: ${projected:.2f} — "
          f"method: measured per-query API spend (${total_cost / n:.4f}, no API "
          f"calls are made; answering is local compute) scaled linearly x"
          f"{10_000 / n:.0f}. Hosting/electricity are not inference spend and "
          f"are excluded.")
    assert total_cost == 0.0, "measured inference spend must be $0 (no API calls)"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
