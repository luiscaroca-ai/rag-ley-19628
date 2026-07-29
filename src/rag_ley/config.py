from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    source_file: Path = ROOT / "data" / "Ley_19628_refundida_21719.txt"
    collection: str = os.getenv("QDRANT_COLLECTION", "ley_21719_rag")
    embed_model: str = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-large")
    embed_dims: int = int(os.getenv("OPENAI_EMBED_DIMS", "256"))
    gen_model: str = os.getenv("OPENAI_GEN_MODEL", "gpt-5.4-mini")
    rerank_model: str = os.getenv("OPENAI_RERANK_MODEL", "gpt-5.4-nano")
    top_k: int = 5
    top_k_wide: int = 20
    threshold: float = float(os.getenv("RAG_THRESHOLD", "0.55"))

    def validate_credentials(self) -> None:
        missing = [name for name in ("OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY") if not os.getenv(name)]
        if missing:
            raise RuntimeError(f"Faltan variables en .env: {', '.join(missing)}")


settings = Settings()

