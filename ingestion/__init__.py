"""Public API for the ingestion layer."""

from .loader import load_text
from .chunker import split_into_chunks

__all__ = ["load_text", "split_into_chunks"]