"""Pure-stdlib TF-IDF retrieval over local documents. No network, no model."""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

_TOKEN = re.compile(r"[a-z0-9]+")
STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "are",
        "what", "how", "do", "does", "for", "on", "at", "by"}


def tokenize(text: str) -> list[str]:
    """Lowercase tokenise and drop stopwords / single characters."""
    return [t for t in _TOKEN.findall(text.lower()) if t not in STOP and len(t) > 1]


@dataclass
class Document:
    """A local document in the index."""

    id: str
    title: str
    text: str


@dataclass
class Hit:
    """A search result: a document plus its cosine score."""

    doc: Document
    score: float


class TfidfIndex:
    """TF-IDF index built in memory from local documents."""

    def __init__(self, docs: list[Document] | None = None) -> None:
        self.docs: list[Document] = []
        self._idf: dict[str, float] = {}
        self._vecs: list[dict[str, float]] = []
        if docs:
            self.build(docs)

    def build(self, docs: list[Document]) -> None:
        """(Re)build the index from ``docs``."""
        self.docs = list(docs)
        n = len(self.docs) or 1
        df: Counter[str] = Counter()
        tfs: list[Counter[str]] = []
        for d in self.docs:
            c = Counter(tokenize(d.title + " " + d.text))
            tfs.append(c)
            for term in c:
                df[term] += 1
        self._idf = {t: math.log((n + 1) / (c + 1)) + 1.0 for t, c in df.items()}
        self._vecs = [self._vec_from_counter(c) for c in tfs]

    def _vec_from_counter(self, c: Counter[str]) -> dict[str, float]:
        total = sum(c.values()) or 1
        vec = {t: (cnt / total) * self._idf.get(t, 1.0) for t, cnt in c.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {t: v / norm for t, v in vec.items()}

    def _query_vec(self, query: str) -> dict[str, float]:
        return self._vec_from_counter(Counter(tokenize(query)))

    def search(self, query: str, k: int = 3) -> list[Hit]:
        """Return the top-``k`` documents by TF-IDF cosine similarity."""
        qv = self._query_vec(query)
        hits: list[Hit] = []
        for doc, dv in zip(self.docs, self._vecs, strict=True):
            score = sum(qv.get(t, 0.0) * w for t, w in dv.items() if t in qv)
            if score > 0:
                hits.append(Hit(doc=doc, score=round(score, 6)))
        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[:k]

    def __len__(self) -> int:
        return len(self.docs)
