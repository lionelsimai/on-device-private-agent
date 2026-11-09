"""Offline agent core: planner -> retrieval -> grounded answer. $0 inference."""
from __future__ import annotations

from dataclasses import dataclass, field

from .planner import plan
from .retrieval import Document, TfidfIndex

DEFAULT_DOCS: list[Document] = [
    Document("privacy", "Privacy model",
             "This agent runs entirely on device. No query leaves the device, no API key "
             "is required, and inference cost is zero. Documents are indexed locally "
             "with TF-IDF."),
    Document("pricing", "Pricing and costs",
             "Inference costs zero dollars because the model runs locally. Hosting a "
             "static page costs almost nothing, so 1000 users still cost $0 in inference."),
    Document("offline", "Offline mode",
             "Offline mode works without internet. The index, planner and browser "
             "fallback all run locally. Service workers can cache the page for full "
             "offline use."),
    Document("quantization", "Quantization guide",
             "Quantization reduces model size. Q4 GGUF models are roughly 4x smaller "
             "than FP16 with a small quality drop and much lower memory use. See the "
             "quantization guide for the size and latency table."),
    Document("browser", "Browser deployment",
             "The browser demo uses WebLLM when WebGPU is available and falls back to "
             "TF-IDF retrieval in vanilla JavaScript when it is not. No download is "
             "required for the fallback."),
]


@dataclass
class Answer:
    """A grounded answer with sources and its (zero) cost."""

    text: str
    intent: str
    sources: list[str] = field(default_factory=list)
    cost_usd: float = 0.0
    offline: bool = True


class PrivateAgent:
    """Offline private agent over a local document set."""

    def __init__(self, docs: list[Document] | None = None) -> None:
        self.index = TfidfIndex(docs if docs is not None else list(DEFAULT_DOCS))

    def add_document(self, doc: Document) -> None:
        """Add a document and rebuild the index."""
        self.index.build([*self.index.docs, doc])

    def ask(self, query: str) -> Answer:
        """Answer ``query`` from local documents only. Cost is always $0."""
        p = plan(query)
        if p.action == "help":
            return Answer(
                text="I answer questions from your local documents, fully offline. "
                     "Ask about a topic, say 'list' for documents, or 'summarise <topic>'.",
                intent=p.intent)
        if p.action == "list":
            titles = ", ".join(d.title for d in self.index.docs)
            return Answer(text=f"Local documents: {titles}.", intent=p.intent,
                          sources=[d.id for d in self.index.docs])
        hits = self.index.search(query, k=3)
        if not hits:
            return Answer(text="No matching local document found. Try different words "
                               "or add the document locally.", intent=p.intent)
        if p.action == "summarise":
            best = hits[0].doc
            first = best.text.split(". ")[0].rstrip(".") + "."
            return Answer(text=first, intent=p.intent, sources=[best.id])
        joined = " ".join(h.doc.text for h in hits[:2])
        return Answer(text=joined, intent=p.intent, sources=[h.doc.id for h in hits])
