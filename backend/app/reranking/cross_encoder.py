import os
import cohere
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv(override=True)

client = cohere.ClientV2(
    api_key=os.environ["COHERE_API_KEY"]
)

@traceable(run_type="chain", name="rerank")
def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 5
) -> list[dict]:

    documents = [c["text"] for c in candidates]

    response = client.rerank(
        model="rerank-v4.0-fast",
        query=query,
        documents=documents,
        top_n=top_k
    )

    reranked = []

    for result in response.results:
        item = candidates[result.index].copy()
        item["rerank_score"] = float(result.relevance_score)
        reranked.append(item)

    return reranked