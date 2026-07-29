from qdrant_client.models import Distance, VectorParams
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os

from rag_ley.chunking import chunk_law
from rag_ley.config import settings


def main() -> None:
    settings.validate_credentials()
    if not settings.source_file.exists():
        raise FileNotFoundError(f"Copia el texto de la ley en: {settings.source_file}")
    documents = chunk_law(settings.source_file.read_text(encoding="utf-8"))
    embeddings = OpenAIEmbeddings(model=settings.embed_model, dimensions=settings.embed_dims)
    client = QdrantClient(url=os.environ["QDRANT_URL"], api_key=os.environ["QDRANT_API_KEY"])
    if client.collection_exists(settings.collection):
        client.delete_collection(settings.collection)
    client.create_collection(
        collection_name=settings.collection,
        vectors_config=VectorParams(size=settings.embed_dims, distance=Distance.COSINE),
    )
    store = QdrantVectorStore(client=client, collection_name=settings.collection, embedding=embeddings)
    store.add_documents(documents)
    print(f"Colección '{settings.collection}' creada con {len(documents)} chunks.")


if __name__ == "__main__":
    main()

