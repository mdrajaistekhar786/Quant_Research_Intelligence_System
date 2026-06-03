# 📊 Quant Research Intelligence System

> *Because reading 50 research papers before making an investment decision shouldn't take 50 hours.*

---

## What is this?

I built this project out of a simple frustration — there's a mountain of quantitative finance research out there, and finding the right paper at the right moment is genuinely painful. This system brings together RAG (Retrieval-Augmented Generation), hybrid search, and a conversational AI interface to let you *talk* to a library of quant research papers like they're a colleague who's actually read all of them.

Ask it something like *"What does the literature say about momentum factor decay?"* and it'll pull the most relevant chunks, re-rank them intelligently, and give you a grounded, cited answer — not a hallucination.

---

## The Stack (and why I chose it)

| Layer | Tool | Why |
|---|---|---|
| 💬 LLM | Groq (Llama 3.3 70B) | Fast inference, great at synthesis |
| 🔍 Retrieval | FAISS + BM25 | Hybrid: semantic + keyword search |
| 🔁 Re-ranking | Cross-encoder | Precision matters in finance |
| 🧠 Embeddings | Sentence Transformers | Open-source, reliable |
| 🖥️ UI | Streamlit | Quick to build, easy to use |
| 📓 Exploration | Jupyter Notebooks | Step-by-step, reproducible |

---

## Project Structure

```
Quant_Research_Intelligence_System/
│
├── app/
│   ├── app.py          # Streamlit front-end
│   └── rag.py          # Core RAG logic
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb       # Load & parse papers
│   ├── 02_chunking.ipynb             # Smart text chunking
│   ├── 03_embeddings.ipynb           # Generate embeddings
│   ├── 04_hybrid_retrieval.ipynb     # BM25 + FAISS search
│   ├── 05_reranking.ipynb            # Cross-encoder re-ranking
│   ├── 06_rag_pipeline.ipynb         # End-to-end RAG pipeline
│   ├── 07_factor_extraction.ipynb    # Extract quant factors
│   ├── 08_research_synthesis.ipynb   # Synthesize findings
│   └── 09_streamlit_app.ipynb        # App prototyping
│
├── data/
│   ├── raw_papers/                   # Source PDFs
│   ├── processed_papers/             # Chunked & embedded
│   ├── vector_store/                 # FAISS index
│   └── factor_database.csv          # Extracted factors
│
├── requirements.txt
└── .gitignore
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/mdrajaistekhar786/Quant_Research_Intelligence_System.git
cd Quant_Research_Intelligence_System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API key

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com)

### 4. Run the notebooks (in order)

Start from `01_data_ingestion.ipynb` and work your way through. Each notebook builds on the last.

### 5. Launch the app

```bash
streamlit run app/app.py
```

---

## How It Works

```
Your Question
     │
     ▼
Hybrid Search (BM25 + FAISS)
     │
     ▼
Top-K Candidate Chunks
     │
     ▼
Cross-Encoder Re-ranking
     │
     ▼
Best Chunks → Groq LLM
     │
     ▼
Grounded, Cited Answer
```

The hybrid search catches both *semantically similar* content (via dense embeddings) and *exact keyword matches* (via BM25) — which matters a lot in finance where terminology is precise.

---

## What Kind of Questions Can You Ask?

- *"Summarize the key findings on value factor performance post-2010"*
- *"What methods are used for factor decay analysis?"*
- *"Which papers discuss momentum crashes and how do they explain them?"*
- *"Compare how different papers define the quality factor"*

---

## Roadmap

- [ ] Add more papers (currently focused on factor investing)
- [ ] Multi-document comparison view
- [ ] Export answers with citations to PDF
- [ ] Support for user-uploaded papers
- [ ] Finer-grained factor taxonomy

---

## A Note on API Keys

Please don't hardcode API keys in notebooks. Use environment variables:

```python
import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
```

---

## About

Built by **Md Raja Istekhar** — a quant researcher who got tired of ctrl+F-ing through PDFs.

Feel free to open an issue, suggest papers to add, or just say hi.

---

*If this saved you time, consider starring the repo ⭐ — it helps more than you'd think.*
