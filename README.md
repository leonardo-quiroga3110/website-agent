---
title: Monte Azul Expert
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Monte Azul Expert Agent (RAG + LangGraph)

A premium, production-ready autonomous agent designed to provide expert-level insights about **Corporación Monte Azul**. This system uses a sophisticated Retrieval-Augmented Generation (RAG) pipeline combined with **Chain-of-Thought (CoT)** reasoning via LangGraph.

## 🚀 Key Features

- **Advanced Ingestion**: Uses **IBM Docling** to scrape and parse the official website, preserving complex structures like tables and layouts.
- **Hybrid Retrieval**: Combines **Semantic Search** (ChromaDB + OpenAI Embeddings) with **Keyword Search** (BM25) for maximum accuracy.
- **Autonomous Reasoning**: Built with **LangGraph**, featuring a multi-node flow (Reflector -> Researcher -> Critic -> Responder) that "thinks" before answering.
- **Premium UI**: Integrated **Gradio** interface for a sleek, interactive chat experience.
- **Production Ready**: Full Docker support for seamless deployment to Hugging Face Spaces.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

### 2. Installation
Install the project dependencies (using `uv` is recommended):
```bash
uv pip install -e .
# or
pip install -e .
```

### 3. Environment Configuration
Copy the example environment file and add your keys:
```bash
cp .env.example .env
```
Edit `.env` and provide:
- `OPENAI_API_KEY`: Your OpenAI API key.
- `TAVILY_API_KEY`: Your Tavily API key (optional for web search).
- `WEBSITE_URL`: The URL to scrape (e.g., `https://www.monteazulgroup.com/es`).


---

## 📂 Data Ingestion (Building the "Knowledge")

To feed the agent with the latest information from the Monte Azul portal, you must run the indexer script.

### The Indexing Tip:
```powershell
$env:PYTHONPATH="src"; python ingest_data.py --clear
```
**Explanation:**
- `$env:PYTHONPATH="src"`: Tells Python to look into the `src` folder for modules (necessary because our code is structured inside `src/agent`).
- `python ingest_data.py`: Executes the indexing script.
- `--clear`: **Crucial Flag**. It wipes the existing local database before re-scraping. Use this if you want to update the agent's knowledge or if the website content has changed.

---

## 🌐 Running Locally

To launch the interactive chat interface:
```bash
python app.py
```
The interface will be available at `http://localhost:7860`.

---

## ☁️ Hugging Face Deployment

To deploy this agent as a **Hugging Face Space**:

1. **Create a Space**: Select **Gradio** as the SDK and choose the **Docker** template.
2. **Upload Files**: Push this entire repository to the Hugging Face Space.
3. **Set Secrets**:
   - Go to **Settings > Variables and Secrets**.
   - Add `OPENAI_API_KEY` (mandatory for embeddings and chat).
4. **Deploy**: The provided `Dockerfile` will automatically install the system dependencies for Docling and launch the app.

---

## 🧠 Reasoning Process
The agent follows an internal **Chain-of-Thought**:
1. **Reflect**: Analyzes the query and current knowledge.
2. **Retrieve**: Pulls relevant chunks from the ChromaDB hybrid index.
3. **Critic**: Evaluates if retrieved data is sufficient.
4. **Respond**: Synthesizes the final answer using the expert Senior Analyst persona.
