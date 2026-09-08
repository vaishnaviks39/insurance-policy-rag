# Insurance Policy RAG

A RAG application for querying insurance policy documents and generating source-grounded answers.

## What it does

- Upload insurance policy PDFs and extract their content
- Retrieve relevant chunks using dense embeddings and BM25
- Combine retrieval results using Reciprocal Rank Fusion (RRF)
- Rerank results with Cohere
- Generate answers with citations to the source pages
- Evaluate retrieval and answer quality with DeepEval
- Trace RAG workflows with LangSmith

## Architecture

PDF → Chunking → Embeddings + BM25 → RRF → Cohere Reranking → GPT → Answer with Sources

## Tech Stack

Python, FastAPI, Streamlit, OpenAI, ChromaDB, BM25, Cohere, DeepEval, LangSmith, Docker, AWS

## Deployment

The application is containerized with Docker and deployed on AWS EC2. Docker images are stored in Amazon ECR.

## Run Locally

Create `backend/.env` with the required API keys.

```bash
docker compose up --build
```

Open `http://localhost:8501`.
