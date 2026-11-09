"""Offline agent core: planner -> retrieval -> grounded answer.

Local compute only — no LLM and no API call is ever made, so the measured
inference cost of an answer is $0 (local CPU time, not a billed API call).
"""
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
             "Inference costs zero dollars because everything runs locally and no "
             "API is called. Hosting a static page costs almost nothing, so 1000 "
             "users still cost $0 in inference."),
    Document("offline", "Offline mode",
             "Offline mode works without internet. The index, planner and browser "
             "fallback all run locally. Service workers can cache the page for full "
             "offline use."),
    Document("quantization", "Quantization guide",
             "Quantization reduces model size. Q4 GGUF models are roughly 4x smaller "
             "than FP16 with a small quality drop and much lower memory use. See the "
             "quantization guide for the size and latency table."),
    Document("browser", "Browser deployment",
             "The browser demo always runs the local TF-IDF fallback in vanilla "
             "JavaScript: no download is required and nothing leaves the device. "
             "A WebLLM integration hook is present in the demo code but is a stub "
             "that returns null, so no LLM runs in the browser demo today."),
]


@dataclass
class Answer:
    """A grounded answer with the sources its text actually uses.

    ``cost_usd`` is the measured inference spend: it is 0.0 because the
    answer is produced by local TF-IDF compute and no API call is made.
    It is a reported measurement of this design, not a billed figure.
    """

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
        """Answer ``query`` from local documents only.

        No network or API call is made, so the measured inference cost is
        $0. ``sources`` lists only the documents whose text is used in the
        answer, never merely-retrieved hits.
        """
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
        used = hits[:2]
        joined = " ".join(h.doc.text for h in used)
        return Answer(text=joined, intent=p.intent, sources=[h.doc.id for h in used])
