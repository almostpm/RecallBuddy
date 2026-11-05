"""Integration tests for the main flow without making real API calls."""

import pytest
from unittest.mock import patch, MagicMock

from progress.tracker import ProgressTracker
from ingestion.chunker import split_into_chunks


def test_chunker_integration():
    chunks = split_into_chunks("A" * 1200, 500)
    assert len(chunks) == 3


def test_progress_tracker_integration(tmp_path):
    tracker = ProgressTracker(log_dir=tmp_path)
    tracker.record_attempt("Math", "What is 2+2?", True)
    tracker.record_attempt("Science", "What is H2O?", False)
    stats = tracker.get_stats()
    assert stats["accuracy"] == 50.0


def test_imports():
    from session.quiz_session import QuizSession
    from quiz.generator import generate_question

    assert QuizSession is not None
    assert generate_question is not None