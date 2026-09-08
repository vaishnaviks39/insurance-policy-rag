from rank_bm25 import BM25Okapi
from langsmith import traceable

class BM25Index:
    def __init__(self, chunks: list[dict]):
        """chunks: [{"text": ..., "meta": ..., "id": ...}, ...]"""
        self.chunks = chunks
        tokenized = [c["text"].lower().split() for c in chunks]
        self.bm25 = BM25Okapi(tokenized)

    @traceable(run_type="retriever", name="bm25_search")
    def search(self, query: str, top_k: int = 10) -> list[dict]:
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        ranked_idx = sorted(range(len(scores)), key=lambda i: -scores[i])[:top_k]
        return [
            {
                "id": self.chunks[i]["id"],
                "text": self.chunks[i]["text"],
                "meta": self.chunks[i]["meta"],
                "score": float(scores[i]),
            }
            for i in ranked_idx
        ]