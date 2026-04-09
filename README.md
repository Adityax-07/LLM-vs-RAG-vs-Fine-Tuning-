# CodeSage — LLM vs RAG vs Fine-Tuning

> A live comparative study of three NLP architectures for domain-specific Q&A, built with Streamlit.

Ask a question once — get answers simultaneously from a **Baseline LLM**, a **RAG Chatbot**, and a **Fine-Tuned model**, with automatic quality metrics on every response.

---

## What It Does

- **Three systems, one question** — side-by-side answers from all three architectures
- **Auto-evaluation metrics** per card: Accuracy, ROUGE-L, Groundedness, Context Relevance, Latency
- **Winner badge** highlights the best answer; **Hallucination badge** flags low-confidence responses
- **Auto-Benchmark runner** evaluates all 50 reference Q&A pairs and stores results permanently to disk (`data/benchmark_cache.json`), so you run it once and the analytics persist across restarts
- **Analytics dashboard** always visible — KPI cards, Plotly bar charts, and a paper-style TABLE II breakdown

---

## Systems

| System | Model | Method |
|--------|-------|--------|
| ⚡ Baseline LLM | Groq API (LLaMA 3) | Direct zero-shot prompting |
| 🔍 RAG Chatbot | LLaMA 3 + FAISS | Retrieval-Augmented Generation |
| 🧠 Fine-Tuned | Qwen2.5-1.5B-Instruct | LoRA fine-tuned on CS Q&A pairs |

---

## Auto-Evaluation Metrics (TABLE II)

| Metric | Description | Unit |
|--------|-------------|------|
| Answer Accuracy | Cosine similarity of answer vs reference embedding | % |
| Groundedness Score | Cosine similarity of answer vs retrieved context | 0–1 |
| Hallucination Rate | % of answers with accuracy < 0.5 | % |
| Answer Relevance | Cosine similarity of answer vs question | 0–1 |
| Faithfulness | ROUGE-L overlap with source context or reference | 0–1 |
| Avg Response Time | Mean latency per query | sec |
| Cost per Query | Token-count-based cost estimate | USD |
| Overall Score (1–5) | Weighted composite: 30% Acc + 20% Ground + 20% (1−HR) + 15% Relevance + 15% Faith | rating |

---

## Knowledge Base (50 Topics)

Covers CS fundamentals, algorithms, web technologies, databases, and tooling:

**Data Structures & Algorithms** — Binary Search, Merge Sort, QuickSort, Linked List, BST, Dynamic Programming, Recursion, Heap, Graph, DFS, BFS, Hash Table / Hash Map, Big O Notation, Trees, Inorder Traversal, Memoization, Stack vs Queue, Time & Space Complexity

**Web & JavaScript** — React Hooks, useState, useEffect, REST API, HTTP Methods, HTTP Status Codes, JavaScript Promises, async/await, Closures, Event Loop, TypeScript

**Styling** — CSS Flexbox, CSS Grid, flex-grow

**Databases & Systems** — SQL, Primary Key, Foreign Key, Indexes, Normalization, Git, Merge Conflicts, Docker, JSON

**OOP** — Inheritance, Polymorphism, Encapsulation, Object-Oriented Programming

---

## Project Structure

```
.
├── demo.py                         # Main Streamlit app
├── system1_baseline.py             # Groq API baseline
├── system2_rag.py                  # FAISS RAG pipeline
├── system3_inference.py            # Fine-tuned model inference
├── system3_finetune_colab.ipynb    # Qwen2.5 fine-tuning notebook (Colab)
├── requirements.txt
├── data/
│   ├── reference_answers.json      # 50 Q&A pairs for auto-evaluation
│   ├── benchmark_cache.json        # Persisted benchmark results (generated on first run)
│   ├── finetune_data.jsonl         # Training data in ChatML format
│   ├── faiss_index/                # FAISS vector store (built automatically)
│   ├── docs/                       # Knowledge base .txt files
│   └── pdfs/                       # Drop PDFs here to ingest into RAG
└── evaluate.py                     # Standalone evaluation script
```

---

## Setup

### 1. Clone & install

```bash
git clone https://github.com/Adityax-07/LLM-vs-RAG-vs-Fine-Tuning-.git
cd LLM-vs-RAG-vs-Fine-Tuning-
pip install -r requirements.txt
```

### 2. Set your API key

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at [console.groq.com](https://console.groq.com).

### 3. Run the app

```bash
streamlit run demo.py
```

The FAISS vector store is built automatically on first launch.

### 4. (Optional) Fine-tune the model

Open `system3_finetune_colab.ipynb` in Google Colab, run all cells, then download the resulting `finetuned_model/` folder and place it in the project root.

### 5. Run the benchmark (once)

Click **Run Auto-Benchmark** in the Analytics tab. Results are saved to `data/benchmark_cache.json` and displayed permanently on every subsequent app load — no need to re-run.

---

## Adding PDFs to the Knowledge Base

Drop any PDF into `data/pdfs/` and restart the app. The RAG pipeline ingests PDFs automatically via `pypdf`.

---

## Tech Stack

| Layer | Library |
|-------|---------|
| UI | Streamlit, Plotly |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector Store | FAISS (via LangChain) |
| LLM API | Groq (LLaMA 3) |
| Fine-Tuning | Hugging Face Transformers + PEFT (LoRA) |
| Metrics | rouge-score, numpy (cosine similarity) |
| PDF Ingestion | pypdf via LangChain |

---

## Deploy on Hugging Face Spaces

```yaml
---
title: CodeSage
emoji: 🧙
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.35.0"
app_file: demo.py
pinned: false
---
```

Add `GROQ_API_KEY` as a Space secret.
