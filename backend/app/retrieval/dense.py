import os
from openai import OpenAI
import chromadb
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv(override=True)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
EMBED_MODEL = "text-embedding-3-small"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Sends a list of strings to OpenAI, gets back a list of embedding
    vectors (one per string).
    """
    response = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]

def get_chroma_collection(collection_name: str, persist_dir: str = "./chroma_store"):
    """
    Opens (or creates) a persistent Chroma database on disk at `persist_dir`.
    """
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    return chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

def index_chunks(chunks: list[dict], collection, doc_id: str):
    """
    chunks: [{"text": "...", "meta": {"page": 1}}, ...]
    Embeds every chunk's text, then stores (text, embedding, metadata, id)
    together in the Chroma collection.
    """
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [c["meta"] for c in chunks]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

@traceable(run_type="retriever", name="dense_search")
def dense_search(query: str, collection, top_k: int = 5) -> list[dict]:
    """
    Embeds the user's question, asks Chroma for the top_k stored chunks
    whose embeddings are closest (most similar in meaning) to the
    question's embedding.
    """
    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    hits = []
    for id_, text, meta, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({
            "id": id_,
            "text": text,
            "meta": meta,
            "score": 1 - distance
        })
    return hits