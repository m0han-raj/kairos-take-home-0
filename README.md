# Kairos Intern Take‑Home: **Scientific‑Paper Scout**

## 0 — Goal

Build an AI “Scientific‑Paper Scout” agent that helps a user discover and summarise recent research papers on any topic. The user interacts with the agent through a **command‑line chat** (`python main.py`). A tiny React front‑end is an **optional stretch goal**.

Everything should run locally on a typical laptop with **Python 3.x**. You may use `venv`, `poetry`, or `conda`—your choice. **Docker is *not* required.**

---

## 1 — Architecture

| Component                                                                                       | Tech                                         | Required behaviour                                                                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Agent Host**                                                                                  | Python 3.x · FastAPI (optionally)           | Receives user messages, decides when/with which arguments to call each MCP server, streams partial responses. Logs every tool call (name, args, timestamps, outcome).                                                                                              |
| **`paper_search` MCP server**                                                                   | Python or Typescript MCP server                       | **Input**: `{ "query": "string", "max_results": int }` → Queries the public arXiv API (no key) and returns ≤ `max_results` items.                                                                           |
| **`pdf_summarize` MCP server**                                                                  | Python or Typescript MCP server                      | **Input**: `{ "pdf_url": "string" }` → Downloads PDF, extracts text and summarises using either (1) a local HF model (e.g. `mistral-7b-instruct-q4` via Ollama) **or** (2) OpenAI. **Output**: `{ "summary": "string" }`. |
| **Interface**                                                                                   | CLI chat (required) · Vite + React (stretch) | Shows streamed assistant responses **and prints each tool call** (name, args, latency) to the console.                                                                                                                                                             |


---

Please feel free to ask any clarifying questions.

**Good luck & have fun!**
