"""Track quiz attempts and persist them to a session log."""

import json
import os
from datetime import datetime
from pathlib import Path


class ProgressTracker:
    def __init__(self, log_dir: str | Path = "progress_logs") -> None:
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.log_dir / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.data = {"session_start": datetime.now().isoformat(), "attempts": []}
        self.save()

    def record_attempt(self, topic: str, question: str, is_correct: bool) -> None:
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("topic must be a non-empty string")
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question must be a non-empty string")
        if not isinstance(is_correct, bool):
            raise TypeError("is_correct must be a boolean")
        self.data["attempts"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "topic": topic,
                "question": question,
                "is_correct": is_correct,
            }
        )
        self.save()

    def get_stats(self) -> dict:
        attempts = self.data["attempts"]
        total = len(attempts)
        if total == 0:
            return {"total": 0, "correct": 0, "accuracy": 0.0}
        correct_count = sum(1 for a in attempts if a["is_correct"])
        return {
            "total": total,
            "correct": correct_count,
            "accuracy": round((correct_count / total) * 100, 2),
        }

    def save(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def load(self, file_path: str | Path) -> None:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Log file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                self.data = json.load(f)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON in log file: {file_path}")