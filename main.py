"""RecallBuddy main entry point."""

import os
from dotenv import load_dotenv
from pathlib import Path

from ingestion.loader import load_text
from ingestion.chunker import split_into_chunks
from config import build_vectorstore
from session.quiz_session import QuizSession

load_dotenv()

if __name__ == "__main__":
    file_path = "data/sample_article.txt"
    if not os.path.exists(file_path):
        print("Error: data/sample_article.txt not found. Please create it and add some text.")
        exit(1)

    print("Loading text and building vector store...")
    text = load_text(file_path)
    chunks = split_into_chunks(text)
    try:
        vectorstore = build_vectorstore(chunks)
    except Exception:
        print("Error: OPENAI_API_KEY is required for embeddings. Please add it to .env.")
        exit(1)

    topic = input("\nEnter the topic you want to be quizzed on: ")
    session = QuizSession(vectorstore, topic)
    session.start()