# LangChain and Ollama

A small project for running [LangChain](https://python.langchain.com/) with local LLMs via [Ollama](https://ollama.com/), with optional [Langfuse](https://langfuse.com/) observability.

## Prerequisites

- **Python** 3.10+
- **uv** ([install](https://docs.astral.sh/uv/getting-started/installation/))
- **Ollama** installed and running locally (default: `http://localhost:11434/`)
- (Optional) A **Langfuse** project for tracing and monitoring

## Setup

1. **Clone and enter the project**

   ```bash
   cd "1. Langchain and Ollama"
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   uv venv
   source .venv/bin/activate   # Linux/macOS
   # or: .venv\Scripts\activate   # Windows
   uv pip install -r requirements.txt
   ```

3. **Configure environment**
   - Copy `.env.example` to `.env`
   - Set `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_BASE_URL` if you use Langfuse
   - Model names and Ollama base URL are in `helpers/common.py`; adjust if needed

4. **Pull Ollama models** (examples used in the notebooks)
   ```bash
   ollama pull qwen2.5:7b
   # Optional: ollama pull gemma3:4b  ollama pull deepseek-r1:1.5b  ollama pull nomic-embed-text:latest
   ```

## Project structure

- **`1_langchain_setup.ipynb`** — LangChain + Ollama setup: `ChatOllama`, system/human messages, prompt templates, and streaming with Langfuse callbacks
- **`2_runnables_lcel.ipynb`** — Runnables and LangChain Expression Language (LCEL)
- **`helpers/common.py`** — Shared config: Ollama `BASE_URL` and model names (e.g. `QWEN_MODEL`, `GEMMA_MODEL`)

## Running the notebooks

1. Start Ollama (e.g. `ollama serve` or ensure the Ollama app is running).
2. Activate the virtual environment and start Jupyter:
   ```bash
   source .venv/bin/activate   # Linux/macOS
   uv run jupyter notebook
   ```
   Or, without activating: `uv run jupyter notebook` (from the project directory).
3. Open `1_langchain_setup.ipynb` or `2_runnables_lcel.ipynb` and run the cells.

## Dependencies

- `langchain` — LangChain core
- `langchain-ollama` — Ollama chat integration
- `langfuse` — Observability and tracing (optional)
- `python-dotenv` — Load `.env` for secrets
