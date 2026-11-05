"""Dataclass representing a single generated quiz question."""

from dataclasses import dataclass


@dataclass
class QuizQuestion:
    question: str
    options: list[str]
    correct_index: int
    explanation: str
    source_chunk: str