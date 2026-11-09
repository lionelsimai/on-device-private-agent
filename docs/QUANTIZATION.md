# Quantization Guide (GGUF / Q4)

Quantization stores weights in fewer bits. GGUF is the llama.cpp format.

| Model (example) | FP16 size | Q4_K_M size | RAM (approx) | Tokens/s (phone, indicative) | Quality note |
|---|---|---|---|---|---|
| 1B params | ~2.0 GB | ~0.7 GB | ~1 GB | 20-40 | Good for retrieval/chat |
| 3B params | ~6.0 GB | ~1.9 GB | ~2.5 GB | 10-20 | Noticeable gain |
| 7B params | ~14 GB | ~4.1 GB | ~5 GB | 4-10 (laptop) | Best local quality |
| 8B params | ~16 GB | ~4.9 GB | ~6 GB | 3-8 (laptop) | Diminishing returns |

Rules of thumb:
- Q4_K_M is the default sweet spot: ~4x smaller than FP16, small perplexity increase.
- Q8 is near-lossless at ~2x FP16 compression; Q3/Q2 degrade fast — avoid below Q4 for production.
- Browser/WebLLM: use the pre-quantized MLC builds (q4f16_1); expect a one-time download, then offline.
- Always benchmark on your target device: latency varies 3-5x across chips.
