import os
from dotenv import load_dotenv
from openai import OpenAI
from langsmith import traceable
from langsmith.wrappers import wrap_openai

load_dotenv(override=True)

client = wrap_openai(OpenAI(api_key=os.environ["OPENAI_API_KEY"]))


def build_context(chunks: list[dict]) -> str:
    blocks = []
    for i, c in enumerate(chunks):
        page = c["meta"].get("page", "unknown")
        blocks.append(f"[SOURCE {i+1} | Page {page}]\n{c['text']}")
    return "\n\n".join(blocks)

@traceable(run_type="chain", name="generate_answer")
def generate_answer(
    question: str,
    retrieved_chunks: list[dict],
    model: str = "gpt-4o-mini"
) -> str:

    context = build_context(retrieved_chunks)

    prompt = f"""
You are an insurance policy question-answering assistant.

Answer the user's question using ONLY the information provided in the
retrieved policy sources.

Instructions:
- Use only the provided sources. Do not use outside knowledge.
- Base every factual claim on the retrieved sources.
- Cite the source immediately after the claim using [SOURCE N].
- If multiple sources support a claim, cite all relevant sources.
- If the sources contain conflicting information, mention the conflict
  and cite the relevant sources.
- If the answer can be determined by combining information across the
  retrieved sources, combine those sources and answer the question.
- Only use the fallback response if the retrieved sources genuinely
  contain no information that answers the question.
- Do not invent policy terms, coverage limits, exclusions, conditions,
  or interpretations.
- Preserve distinctions made in the policy between coverage,
  exclusions, conditions, and the category or insured event under
  which a benefit is payable.
- If the policy specifies that a benefit is payable under one category
  or insured event rather than another, state that distinction clearly.
- Answer clearly and directly.
- Do not mention the retrieval process or embedding system.

RETRIEVED POLICY SOURCES:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )

    return response.choices[0].message.content