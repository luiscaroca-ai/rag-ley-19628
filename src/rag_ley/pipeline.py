from __future__ import annotations

import os

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient

from .config import Settings, settings


class Relevance(BaseModel):
    score: float = Field(ge=0.0, le=1.0)


def format_context(documents: list[Document]) -> str:
    return "\n\n".join(
        f"[{doc.metadata.get('articulo', '?')}] {doc.page_content}" for doc in documents
    )


class LegalRAG:
    def __init__(self, config: Settings = settings) -> None:
        config.validate_credentials()
        self.config = config
        self.embeddings = OpenAIEmbeddings(model=config.embed_model, dimensions=config.embed_dims)
        self.client = QdrantClient(url=os.environ["QDRANT_URL"], api_key=os.environ["QDRANT_API_KEY"])
        self.store = QdrantVectorStore(
            client=self.client,
            collection_name=config.collection,
            embedding=self.embeddings,
        )
        answer_prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un asistente legal. Responde usando exclusivamente el contexto. "
             "Si la respuesta no aparece, responde solo 'No se encuentra en el documento.'. "
             "Sé conciso y cita el artículo entre corchetes tal como aparece en el contexto."),
            ("human", "CONTEXTO:\n{contexto}\n\nPREGUNTA: {pregunta}"),
        ])
        self.answer_chain = answer_prompt | ChatOpenAI(model=config.gen_model, reasoning_effort="low") | StrOutputParser()
        rerank_prompt = ChatPromptTemplate.from_messages([
            ("system", "Evalúa de 0 a 1 cuánto ayuda el pasaje a responder la pregunta legal. "
             "Puntúa alto las definiciones, listas y enumeraciones que contengan la respuesta."),
            ("human", "PREGUNTA: {pregunta}\n\nPASAJE: {pasaje}"),
        ])
        self.scorer = rerank_prompt | ChatOpenAI(model=config.rerank_model).with_structured_output(Relevance)

    def answer(self, question: str, rerank: bool = True) -> str:
        if not question.strip():
            return "Escribe una pregunta sobre la ley."
        documents = self._reranked_documents(question) if rerank else self.store.similarity_search(question, k=self.config.top_k)
        if not documents:
            return "No se encuentra en el documento."
        return self.answer_chain.invoke({"contexto": format_context(documents), "pregunta": question})

    def _reranked_documents(self, question: str) -> list[Document]:
        candidates = self.store.similarity_search(question, k=self.config.top_k_wide)
        inputs = [{"pregunta": question, "pasaje": doc.page_content} for doc in candidates]
        scores = [result.score for result in self.scorer.batch(inputs)]
        ranked = sorted(zip(candidates, scores), key=lambda item: item[1], reverse=True)
        return [doc for doc, score in ranked if score >= self.config.threshold]

