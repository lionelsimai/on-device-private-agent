# Changelog

All notable changes to this project will be documented in this file.
Format: Keep a Changelog. Versioning: Semantic Versioning.

## [0.1.1] - 2026-11-09
### Fixed
- Corpus honesty: the built-in "browser" document claimed the demo "uses WebLLM when WebGPU is available". The WebLLM hook is a stub that returns null; the document, `browser/app.js` comments and docs now say the demo always runs the local fallback, and the JS fallback is described as a simplified version of the Python retrieval, not identical logic.
- `Answer.sources` now lists only documents whose text is used in the answer (previously it listed every retrieved hit, including unused ones).
- Bare CLI invocation (`private-agent` with no subcommand) now prints usage and exits with code 2 instead of silently running the demo.
### Changed
- README banner leads honestly ("local retrieval agent — no LLM, no API bill"); the $0 figure is presented as measured per-query API spend ($0.0000 — no API calls are made), with the 1,000-user projection showing its linear-scaling method in the benchmark output.
- Benchmark: 24 queries (was 5) with a proper nearest-rank p95 (was the 4th of 5 samples). Measured after: accuracy 24/24, mean 0.10 ms, p95 0.07 ms, max 1.71 ms (was 5/5, mean 0.04 ms on the old 5-query set).
- `docs/QUANTIZATION.md` labelled as an integration guide for models not bundled with this project.

## [0.1.0] - 2026-11-09
### Added
- Initial public release: working offline demo, CLI, tests, benchmarks, CI gate.
- README with architecture diagram, benchmark section and honest limitations.
