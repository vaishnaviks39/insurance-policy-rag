from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
)

JUDGE_MODEL = "gpt-4o-mini"


def get_rag_metrics():
    return [
        AnswerRelevancyMetric(threshold=0.7, model=JUDGE_MODEL, include_reason=True),
        #FaithfulnessMetric(threshold=0.8, model=JUDGE_MODEL, include_reason=False),
        ContextualPrecisionMetric(threshold=0.7, model=JUDGE_MODEL, include_reason=True),
        ContextualRecallMetric(threshold=0.7, model=JUDGE_MODEL, include_reason=True),
        #ContextualRelevancyMetric(threshold=0.6, model=JUDGE_MODEL, include_reason=True),
    ]