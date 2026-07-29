from rag_ley.chunking import chunk_law


def test_chunking_preserves_article_metadata() -> None:
    text = "Artículo 1°.- Objeto. Texto breve.\nArtículo 2°.- Definiciones. Otro texto."
    docs = chunk_law(text)
    assert len(docs) == 2
    assert docs[0].metadata["articulo"] == "Artículo 1°"
    assert docs[1].metadata["articulo"] == "Artículo 2°"

