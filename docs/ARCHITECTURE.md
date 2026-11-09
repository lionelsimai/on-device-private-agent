# Architecture

```mermaid
flowchart LR
  Q[Query] --> P[Rule planner: intent]
  P --> R[TF-IDF index over local docs]
  R --> A[Grounded answer + source ids, cost $0]
  B[Browser: WebLLM hook — stub, returns null] -.-> R
  B2[Browser engine today: simplified vanilla-JS term-overlap fallback] -.-> R
```

## Components
- **Planner** (`planner.py`): deterministic rules -> intent/action. No LLM, no cost, fully auditable.
- **Retrieval** (`retrieval.py`): TF-IDF over local documents, cosine similarity, stdlib only.
- **Core** (`core.py`): planner -> retrieval -> grounded answer. `sources` lists only the documents whose text the answer uses; `cost_usd` reports the measured inference spend, which is 0.0 because no API call is made.
- **Browser** (`browser/app.js`): always runs a simplified vanilla-JS term-overlap fallback (not identical logic to the Python TF-IDF core). The WebLLM hook is a stub that returns null unconditionally, so no LLM runs in the browser today. Works from `file://` and offline.
- **Config** (`config.py`): environment-based settings (`PRIVATE_AGENT_*`), no hardcoded secrets.

## Privacy architecture
- Data stays on device: documents, index and queries never leave the machine.
- No API keys, no telemetry, no network calls in the Python core.
- Threat model: protects against cloud data exposure and per-token billing; it does not protect against a compromised device OS — use full-disk encryption.
- For a real LLM on device, load a Q4 GGUF / WebLLM model locally (see QUANTIZATION.md); weights are fetched once (or sideloaded) and inference stays local.

## Cost model
Static hosting only. Inference is local compute and no API calls are made, so
the *measured* marginal inference spend per query is $0.0000; the benchmark
projects 1,000 users × 10 queries by scaling that measured figure linearly.
Hosting and electricity are real costs of running devices, but they are not
inference spend and are excluded from the figure.
