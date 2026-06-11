# Athena

A personal knowledge base assistant. Ask questions, get answers grounded in your own notes.

Athena is a local-first RAG (Retrieval-Augmented Generation) pipeline that ingests Markdown files, embeds them into a vector store, and lets you query them via a simple HTTP API. Everything runs on your machine — no cloud required.

> This is v1: a minimal, working baseline. The goal is to build on this iteratively.

---

## Motivation

My Obsidian vault is essentially a dump of notes accumulated over time. Opening it and manually searching for something works, but I wanted a better way — just ask a question and get an answer grounded in what I've actually written.

Beyond that, the decision to expose Athena as an HTTP API rather than a standalone CLI was deliberate. A server means anything can talk to it. The plan is to build multiple clients on top of the same backend: a CLI for the terminal, an Obsidian plugin for in-vault queries, and an integration with a custom shell I'm working on. The core RAG logic stays in one place; the interface is just a matter of what you bolt on.

---

## How it works

```
Your notes (Markdown)
        │
        ▼
  [Ingest endpoint]
        │
        ├─ Reads files modified since last run
        ├─ Parses and chunks Markdown
        ├─ Embeds chunks via Ollama
        └─ Stores vectors in Qdrant
        
  [Query endpoint]
        │
        ├─ Embeds your question
        ├─ Retrieves relevant chunks from Qdrant
        └─ Generates an answer via Ollama LLM
```

---

## Stack

| Component | Tool |
|---|---|
| API | FastAPI |
| Embeddings | Ollama (`nomic-embed-text`) |
| LLM | Ollama (`qwen3:4b`) |
| Vector store | Qdrant |
| Orchestration | LlamaIndex |

---

## Design decisions

**LlamaIndex over LangChain**

Both are common choices for RAG. LangChain is the more general framework — it's highly modular and extends well into agentic AI use cases. LlamaIndex is purpose-built for RAG. Since Athena's goal is straightforward retrieval over personal notes rather than general-purpose AI orchestration, LlamaIndex was the more appropriate fit.

**Local models via Ollama**

Cost and privacy. Running models locally means no API bills and no personal notes leaving your machine — a reasonable tradeoff for a personal knowledge base. The config is model-agnostic, so swapping in a different Ollama model is a one-line change.

**Qdrant for the vector store**

Pragmatic choice for v1. Qdrant is well-documented, has a straightforward Python client, and runs easily in Docker. The abstraction layer from LlamaIndex means the vector store could be swapped out without significant rework if needed.

**FastAPI over Flask**

FastAPI's simplicity, automatic request validation via Pydantic, and async support made it the obvious choice. The config and request models are already typed with Pydantic, so the integration is clean.

**API-first over a standalone script**

A single CLI script would have been simpler for v1, but it would mean rewriting the core logic every time a new interface is needed. Wrapping the pipeline in a server means a CLI, an Obsidian plugin, or a shell integration can all be built independently and talk to the same backend.

---

## Prerequisites

- [Ollama](https://ollama.com) running locally with the required models pulled:
  ```bash
  ollama pull nomic-embed-text
  ollama pull qwen3:4b
  ```
- [Qdrant](https://qdrant.tech/documentation/quick-start/) running locally:
  ```bash
  docker run -p 6333:6333 qdrant/qdrant
  ```
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

---

## Setup

```bash
git clone https://github.com/your-username/athena.git
cd athena

uv sync
```

Configure Athena by editing `config.toml`:

```toml
[ingestion]
src_dir = "./your-notes-directory/"
state_file = "./state.json"

[embedding]
model_name = "nomic-embed-text"
base_url = "http://localhost:11434"

[qdrant]
url = "http://localhost:6333/"
collection_name = "athena"

[llm]
model_name = "qwen3:4b"
url = "http://localhost:11434"
context_window = 8192
request_timeout = 120.0
```

---

## Usage

Start the API server:

```bash
uv run fastapi dev main.py
```

**Ingest your notes:**

```bash
curl -X POST http://localhost:8000/ingest
```

Athena tracks a timestamp in `state.json` and only processes files modified since the last run, so subsequent ingestion calls are fast.

**Ask a question:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What did I write about chunking strategies?"}'
```

**Health check:**

```bash
curl http://localhost:8000/health
```

---

## Project structure

```
athena/
├── core/
│   ├── config.py        # Config schema and loader (TOML)
│   └── clients.py       # Initialises Ollama and Qdrant clients
├── ingest/
│   └── pipeline.py      # Ingestion logic (load → chunk → embed → store)
├── retrieval/
│   └── pipeline.py      # Query logic (embed → retrieve → generate)
├── main.py              # FastAPI app and route definitions
├── config.toml          # Local configuration (gitignored)
└── state.json           # Tracks last ingestion timestamp
```

---

## Known limitations & what's next

The current chunking strategy splits notes by Markdown headers. It's naive — a section under a single heading could be arbitrarily long, and there's no guarantee chunks carry enough context to be independently useful. Better chunking is the main focus for v2, but improving it meaningfully requires proper evaluation: a baseline, test queries with known expected answers, and metrics to measure against. That groundwork comes first.

Beyond chunking, the broader roadmap:

- [ ] CLI client
- [ ] Obsidian plugin
- [ ] Custom shell integration
- [ ] Chat history and multi-turn conversation
- [ ] Support for additional file formats (PDF, DOCX)
- [ ] Re-ranking retrieved chunks before generation
- [ ] Metadata filtering at query time
- [ ] Docker Compose setup for one-command startup

---

## License

MIT
