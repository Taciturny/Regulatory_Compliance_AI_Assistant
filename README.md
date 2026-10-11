# CivicData — Nigerian Data Protection Assistant

CivicData helps people understand Nigerian data protection rights and review pasted privacy notices or terms for clauses that may deserve attention. It is an informational assistant, not a lawyer, and does not provide legal advice or definitive legal determinations.

## Current architecture

- **FastAPI + Uvicorn** serves the application.
- **RAG** retrieves relevant provisions from the NDPA 2023 and GAID 2025 corpus using Pinecone vector search. Pinecone Inference (`llama-text-embed-v2`) creates passage and query embeddings. Gemini generates a plain-language, cited response from the retrieved passages; Cohere Chat is used as a backup if Gemini errors, times out, or returns an unusable response.
- **No conversation database**: pasted terms/questions are not written to CivicData storage or indexed. Text is sent to Pinecone for retrieval and to Gemini; if Gemini fails, the same prompt and retrieved legal passages are sent to Cohere for generation. Avoid entering confidential or identifying details; review both providers' current privacy terms before public launch.
- **Defensive defaults**: server-side secrets, input size limits, security headers, no public API docs, a shared request cap, and bounded concurrent AI requests.

## Run locally

Requires Python 3.10 or newer, a Google AI Studio API key, and a Pinecone account/API key. Defaults preserve the original project index name `regulatoryai`, AWS cloud, and `us-east-1` region. The reset command recreates that index for Pinecone Inference embeddings at 1024 dimensions and cosine similarity; the old 384-dimensional dot-product vectors are not compatible and are regenerated.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your keys to `.env` (never commit it):

```dotenv
LLM_API_KEY=your_google_ai_studio_api_key
LLM_MODEL=gemini-flash-latest
COHERE_API_KEY=your_cohere_api_key
COHERE_MODEL=command-a-plus-05-2026
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=regulatoryai
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
```

The corpus validator checks the numbered source coverage without contacting a service:

```powershell
python -c "from pathlib import Path; from app.legal_corpus import validate_legal_corpus; print(validate_legal_corpus(Path('documents')))"
```

To replace the entire existing Pinecone index and recreate every embedding, run `python -m app.index_legal_sources --reset-index`. This permanently deletes all data in the configured Pinecone index before recreating it. To preserve the index container and replace only CivicData's vectors, run `python -m app.index_legal_sources --rebuild`. Then run `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` and open <http://127.0.0.1:8000>. Do not run the index builder at every server start. Embeddings are generated from `title + content`; both fields are stored in Pinecone metadata and sent to the answer model as retrieved law excerpts.

## Deploy

The repository includes a Render Blueprint in `render.yaml`. Connect the repository in Render and create the web service. Set `LLM_API_KEY`, `COHERE_API_KEY` (for backup generation), and `PINECONE_API_KEY` as Render secrets. Before deploying, run `python -m app.index_legal_sources --reset-index` from a trusted local environment with the same Pinecone key, index name, cloud and region. The web process does not rebuild the index at startup.

Render's free service may sleep when idle and has limited CPU and memory; it is suitable for a small demo, not reliable high-concurrency production. Gemini and Pinecone free quotas can change and are not guaranteed capacity. The default app-side cap of 10 requests/minute and 3 simultaneous AI requests is conservative; tune `CHAT_REQUESTS_PER_MINUTE` and `MAX_CONCURRENT_CHAT_REQUESTS` to observed provider quotas. Requests over the cap receive HTTP 429. Do not advertise support for 300 concurrent users until load-tested against the chosen host and provider quotas.

For a public service, use always-on managed hosting, HTTPS, monitoring, legal-corpus change control, abuse protection, and a reviewed privacy notice. Free Gemini tiers may have data-use terms unsuitable for sensitive user information.

## Model, privacy and security

Gemini and Cohere are called through their native REST APIs. Gemini is always tried first; Cohere is called only when Gemini is unavailable or returns an unusable response. Keep `LLM_API_KEY`, `COHERE_API_KEY`, and `PINECONE_API_KEY` only in `.env` locally or the hosting provider's secret manager. The Gemini key previously pasted into a chat should be revoked and replaced before public deployment.

Pasted text is sent to Pinecone for query embedding and to Gemini for answer generation. If Gemini fails, the prompt and retrieved legal passages are sent to Cohere instead. CivicData does not save pasted text. Avoid entering confidential or identifying details. The server enforces message size limits and security headers; AI findings are issues to investigate, not legal conclusions. Have a qualified Nigerian privacy professional review important decisions.

## Legal corpus

The indexed corpus includes all **65 NDPA sections**, all **52 GAID articles**, and all **10 GAID schedules**. It also includes a separately labeled NDPC DPO-training page to answer career-path questions; those cohort admission criteria are guidance for that programme, not statutory qualification rules. The original NDPA PDF, the complete official 117-page GAID PDF, extracted GAID text, and structured records are in `documents/`. The corpus validator enforces sequence completeness and checks key DPO provisions before indexing. Confirm sources against current NDPC publications when updating; retrieval still cannot guarantee every issue is found or that an answer is legally correct.

Primary sources: [Nigeria Data Protection Act 2023 — NDPC](https://www.ndpc.gov.ng/ndp-act-2023/) · [NDP Act GAID 2025 — NDPC](https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf)

## Project layout

```text
app/main.py                 FastAPI, Gemini, request limits and security headers
app/vector_store.py         Pinecone embedding and semantic retrieval
app/index_legal_sources.py  One-time Pinecone corpus indexing command
app/legal_corpus.py         Offline source-coverage checks before indexing
app/templates/index.html
app/static/css/app.css
app/static/js/app.js
documents/                   Complete NDPA / GAID text, PDFs and structured corpus
render.yaml                  Render deployment blueprint
```

See [LICENSE](LICENSE).
