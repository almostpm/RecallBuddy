"""Read a UTF-8 text file and return its content."""

from pathlib import Path
from pypdf import PdfReader


def load_text(path: str | Path) -> str:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if path.is_dir():
        raise IsADirectoryError(f"Expected a file, got a directory: {path}")
    content = path.read_text(encoding="utf-8", errors="strict")
    if not content.strip():
        raise ValueError(f"Input file is empty: {path}")
    return content


def load_pdf_text(file_path: str | Path) -> str:
    """Extract text from a PDF file using pypdf."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")
    if not path.suffix.lower() == ".pdf":
        raise ValueError(f"File is not a PDF: {path}")

    reader = PdfReader(path)
    text_parts = []
    for page_num, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        except Exception:
            # Some pages may not have extractable text
            continue

    if not text_parts:
        raise ValueError(f"Could not extract any text from PDF: {path}")

    return "\n".join(text_parts)