from langsmith import traceable

def reciprocal_rank_fusion(result_lists: list[list[dict]], k: int = 60, top_k: int = 10) -> list[dict]:
    """
    Combines multiple ranked lists (e.g. dense + BM25) into one fused ranking.
    """
    scores = {}
    lookup = {}

    for result_list in result_lists:
        for rank, item in enumerate(result_list):
            key = item["id"]
            lookup[key] = item
            scores[key] = scores.get(key, 0) + 1 / (k + rank + 1)

    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
    return [{**lookup[key], "rrf_score": score} for key, score in ranked]

@traceable(run_type="chain", name="hybrid_rrf")
def hybrid_search(query: str, dense_fn, bm25_index, top_k: int = 10, candidate_k: int = 20) -> list[dict]:
    """
    dense_fn: a callable(query, top_k) -> list[dict], e.g.
    functools.partial(dense_search, collection=collection)
    """
    dense_results = dense_fn(query, top_k=candidate_k)
    bm25_results = bm25_index.search(query, candidate_k)
    return reciprocal_rank_fusion([dense_results, bm25_results], top_k=top_k)