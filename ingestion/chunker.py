"""Split text into sentence-aware chunks."""

import re


def split_into_chunks(text: str, chunk_size: int = 500) -> list[str]:
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not isinstance(chunk_size, int):
        raise TypeError("chunk_size must be int")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")

    normalized = " ".join(text.split())
    if not normalized:
        return []

    sentences = re.split(r'(?<=[.!?])\s+', normalized)

    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        if current:
            if len(current) + 1 + len(sentence) <= chunk_size:
                current = current + " " + sentence
                continue
            chunks.append(current)
            current = ""
        if len(sentence) <= chunk_size:
            current = sentence
        else:
            for i in range(0, len(sentence), chunk_size):
                chunks.append(sentence[i:i + chunk_size])

    if current:
        chunks.append(current)

    return [chunk.strip() for chunk in chunks if chunk.strip()]