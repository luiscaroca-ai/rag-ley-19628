from __future__ import annotations

import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

ARTICLE_PATTERN = re.compile(
    r"(?=Artículo\s+(?:primero|segundo|tercero|cuarto|quinto|sexto|séptimo|octavo|noveno|décimo|\d+\s*[°º]?)"
    r"(?:\s+(?:bis|ter|quáter|quinquies|sexies))?)"
)


def _article_label(block: str) -> str:
    match = re.match(r"(Artículo\s+[^\n\.\-]{1,20})", block)
    return match.group(1).strip() if match else "Preámbulo"


def _heading(block: str) -> str:
    match = re.match(r"(Artículo\s+[^\n]{1,45}?\.-\s*[^\.\n]{1,60}?\.)", block)
    return match.group(1).strip() if match else _article_label(block)


def chunk_law(text: str, chunk_size: int = 1200, overlap: int = 150, limit: int = 1500) -> list[Document]:
    """Divide por artículo y solo subdivide los artículos extensos."""
    blocks = [block.strip() for block in ARTICLE_PATTERN.split(text) if block.strip()]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    documents: list[Document] = []
    for block in blocks:
        article = _article_label(block)
        heading = _heading(block)
        parts = [block] if len(block) <= limit else splitter.split_text(block)
        for index, part in enumerate(parts, start=1):
            content = part if part.startswith("Artículo") else f"[{heading}] {part}"
            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": "Ley 19.628 (ref. 21.719)",
                        "articulo": article,
                        "parte": f"{index}/{len(parts)}",
                    },
                )
            )
    return documents

