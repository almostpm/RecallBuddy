"""Build an in-memory vector store from text chunks."""

import os

from educhain.core.vectorstore import InMemoryVectorStore
from educhain.models.llm import ChatModel
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

DEFAULT_CHUNK_SIZE: int = 500

# Groq models in priority order - if primary hits rate limit, try fallback
# Verified working via Groq API as of 2026-11-05
GROQ_MODELS = ["openai/gpt-oss-20b", "qwen/qwen3.8-27b", "openai/gpt-oss-120b"]


def build_vectorstore(chunks: list[str]) -> InMemoryVectorStore:
    if not isinstance(chunks, list):
        raise TypeError("chunks must be a list")
    if len(chunks) == 0:
        raise ValueError("chunks list is empty")

    embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    store = InMemoryVectorStore(embedding_model=embedding_model)
    store.add_texts(chunks)
    return store


def get_chat_model(model_name: str = "openai/gpt-oss-120b") -> ChatModel:
    if "GROQ_API_KEY" in os.environ:
        from langchain_openai import ChatOpenAI

        return ChatModel(
            model=ChatOpenAI(
                model_name=model_name,
                api_key=os.environ["GROQ_API_KEY"],
                base_url="https://api.groq.com/openai/v1",
            )
        )
    if "OPENAI_API_KEY" in os.environ:
        return ChatModel()
    raise ValueError(
        "No API key found. Set GROQ_API_KEY or OPENAI_API_KEY in your .env file."
    )