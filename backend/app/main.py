import os
import uuid

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from functools import partial

from app.ingestion.pdf_loader import build_page_documents
from app.chunking.chunking import chunk_pages
from app.retrieval.dense import get_chroma_collection, index_chunks, dense_search
from app.retrieval.bm25 import BM25Index
from app.retrieval.hybrid import hybrid_search
from app.reranking.cross_encoder import rerank
from app.retrieval.hybrid import reciprocal_rank_fusion
from app.generation.generate import generate_answer

from langsmith import traceable

load_dotenv(override=True)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DOCS = {}  # doc_id -> chunks, Chroma collection, and BM25 index


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())[:8]

    os.makedirs("data/raw", exist_ok=True)
    raw_path = f"data/raw/{doc_id}.pdf"
    with open(raw_path, "wb") as f:
        f.write(await file.read())

    page_docs = build_page_documents(raw_path)
    chunks = chunk_pages(page_docs)

    collection = get_chroma_collection(collection_name=doc_id)
    index_chunks(chunks, collection, doc_id)
    bm25_chunks = [
    {
        **chunk,
        "id": f"{doc_id}_chunk_{i}"
    }
    for i, chunk in enumerate(chunks)
    ]   

    bm25_index = BM25Index(bm25_chunks)

    DOCS[doc_id] = {
        "chunks": bm25_chunks,
        "collection": collection,
        "bm25": bm25_index
    }

    return {"doc_id": doc_id, "num_chunks": len(chunks)}

@app.get("/search")
async def search(doc_id: str, query: str, top_k: int = 5):
    """Dense-only search (kept for debugging/comparison)."""
    if doc_id not in DOCS:
        return {"error": f"no document found with id {doc_id}"}
    collection = DOCS[doc_id]["collection"]
    results = dense_search(query, collection, top_k)
    return {"query": query, "results": results}

@traceable(run_type="chain", name="rag_chat")
@app.post("/chat")
async def chat(doc_id: str, question: str):
    """Full pipeline: hybrid search (dense + BM25 + RRF) -> rerank -> generate."""
    if doc_id not in DOCS:
        return {"error": f"no document found with id {doc_id}"}

    doc = DOCS[doc_id]
    dense_fn = partial(dense_search, collection=doc["collection"])

    candidates = hybrid_search(question, dense_fn, doc["bm25"], top_k=20, candidate_k=20)
    top_chunks = rerank(question, candidates, top_k=5)
    answer = generate_answer(question, top_chunks)

    import re
    cited_numbers = set(int(n) for n in re.findall(r'\[SOURCE (\d+)\]', answer))
    filtered_sources = [
        {"page": c["meta"].get("page"), "text": c["text"][:150]}
        for i, c in enumerate(top_chunks)
        if (i + 1) in cited_numbers
    ]

    seen_texts = set()
    unique_sources = []
    for src in filtered_sources:
        text_key = " ".join(src["text"].split())
        if text_key not in seen_texts:
            seen_texts.add(text_key)
            unique_sources.append(src)

    seen_debug_texts = set()
    debug_chunks = []
    for c in top_chunks:
        text_key = " ".join(c["text"].split())
        if text_key not in seen_debug_texts:
            seen_debug_texts.add(text_key)
            debug_chunks.append({"page": c["meta"].get("page"), "text": c["text"]})

    return {"answer": answer, "sources": unique_sources, "retrieved_chunks": debug_chunks}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/debug_retrieval")
async def debug_retrieval(doc_id: str, query: str):
    if doc_id not in DOCS:
        return {"error": f"no document found with id {doc_id}"}

    doc = DOCS[doc_id]

    dense_results = dense_search(query, doc["collection"], top_k=10)
    bm25_results = doc["bm25"].search(query, top_k=10)
    fused = reciprocal_rank_fusion([dense_results, bm25_results], top_k=10)
    reranked = rerank(query, fused, top_k=5)

    return {
        "dense_top_10": [{"id": r["id"], "score": round(r["score"], 4), "text": r["text"][:80]} for r in dense_results],
        "bm25_top_10": [{"id": r["id"], "score": round(r["score"], 4), "text": r["text"][:80]} for r in bm25_results],
        "fused_top_10": [{"id": r["id"], "rrf_score": round(r["rrf_score"], 5), "text": r["text"][:80]} for r in fused],
        "reranked_top_5": [{"score": round(r["rerank_score"], 4), "text": r["text"][:80]} for r in reranked],
    }