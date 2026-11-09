"""On-device private agent — offline, $0 inference."""
from .core import Answer, PrivateAgent
from .retrieval import Document, TfidfIndex

__all__ = ["PrivateAgent", "Answer", "TfidfIndex", "Document"]
__version__ = "0.1.1"
