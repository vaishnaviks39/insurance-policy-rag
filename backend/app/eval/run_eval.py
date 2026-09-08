import json
import time
from collections import defaultdict

from dotenv import load_dotenv
load_dotenv(override=True)

import os

os.environ["DEEPEVAL_PER_TASK_TIMEOUT_SECONDS_OVERRIDE"] = "600"
os.environ["DEEPEVAL_RETRY_MAX_ATTEMPTS"] = "2"

import requests
from deepeval import evaluate
from deepeval.evaluate.configs import AsyncConfig, DisplayConfig
from deepeval.test_case import LLMTestCase

from eval_set import EVAL_SET, DOC_ID
from deepeval_metrics import get_rag_metrics

BACKEND_URL = "http://localhost:8000"


def call_chat(doc_id, question):
    resp = requests.post(
        f"{BACKEND_URL}/chat",
        params={"doc_id": doc_id, "question": question, "debug": True},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


def build_test_cases(doc_id):
    test_cases = []
    for case in EVAL_SET:
        result = call_chat(doc_id, case["question"])
        answer = result.get("answer") or ""
        retrieval_context = [c["text"] for c in result.get("retrieved_chunks", [])] or [""]

        if not answer:
            print(f"[WARN] empty answer for id={case['id']!r} question={case['question']!r}")
            print(f"        raw response: {result}")

        test_cases.append(LLMTestCase(
            input=case["question"],
            actual_output=answer or "[NO ANSWER RETURNED]",
            expected_output=case["expected_answer"],
            retrieval_context=retrieval_context,
            additional_metadata={"id": case["id"], "category": case["category"]},
        ))
        time.sleep(7)
    return test_cases


def flatten_results(test_cases, eval_result):
    rows = []
    for tc, res in zip(test_cases, eval_result.test_results):
        for m in res.metrics_data:
            rows.append({
                "id": tc.metadata["id"],
                "category": tc.metadata["category"],
                "question": tc.input,
                "metric": m.name,
                "score": round(m.score, 4) if m.score is not None else None,
                "passed": m.success,
                "reason": m.reason,
            })
    return rows


def print_summary(rows):
    by_category = defaultdict(lambda: [0, 0])
    by_metric = defaultdict(lambda: [0, 0])

    for r in rows:
        by_category[r["category"]][1] += 1
        by_metric[r["metric"]][1] += 1
        if r["passed"]:
            by_category[r["category"]][0] += 1
            by_metric[r["metric"]][0] += 1

    print("\n=== Pass rate by category ===")
    for cat, (passed, total) in sorted(by_category.items()):
        print(f"  {cat:24s} {passed}/{total}")

    print("\n=== Pass rate by metric ===")
    for metric, (passed, total) in sorted(by_metric.items()):
        print(f"  {metric:24s} {passed}/{total}")

    failing = [r for r in rows if not r["passed"]]
    if failing:
        print(f"\n=== {len(failing)} failing ===")
        for r in failing:
            print(f"  [{r['id']}] {r['metric']} = {r['score']} -- {r['question']}")


def main():
    if DOC_ID == "REPLACE_WITH_UPLOADED_DOC_ID":
        raise SystemExit("Set DOC_ID in eval_set.py first.")

    test_cases = build_test_cases(DOC_ID)
    eval_result = evaluate(
        test_cases=test_cases,
        metrics=get_rag_metrics(),
        async_config=AsyncConfig(run_async=False),
        display_config=DisplayConfig(show_indicator=True, print_results=True),
    )

    rows = flatten_results(test_cases, eval_result)
    with open("eval_results.json", "w") as f:
        json.dump(rows, f, indent=2)

    print_summary(rows)
    print(f"\nSaved {len(rows)} rows to eval_results.json")


if __name__ == "__main__":
    main()