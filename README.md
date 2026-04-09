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

## Benchmark Results (n = 50 questions)

| Metric | Baseline LLM | RAG Chatbot | Fine-Tuned | Unit |
|--------|-------------|-------------|------------|------|
| Answer Accuracy | 81.5 | 79.9 | — | % |
| ROUGE-L | 0.216 | 0.291 | — | 0–1 |
| Groundedness | 0.815 | 0.575 | — | 0–1 |
| Answer Relevance | 0.720 | 0.768 | — | 0–1 |
| Faithfulness | 0.216 | 0.172 | — | 0–1 |
| Hallucination Rate | 0.0 | 6.0 | — | % |
| Avg Response Time | 1.46 | 4.19 | — | sec |
| Cost per Query | $0.0020 | $0.0020 | — | USD |

> Fine-Tuned column shows `—` until `finetuned_model/` is placed in the project root (see Setup §4).  
> Full per-question results are in `data/benchmark_cache.json`.

---

## Project Structure

```
.
├── demo.py                         # Main Streamlit app
├── system1_baseline.py             # Groq API baseline
├── system2_rag.py                  # FAISS RAG pipeline
├── system3_inference.py            # Fine-tuned model inference
├── system3_finetune_colab.ipynb    # Qwen2.5 fine-tuning notebook (Colab)
├── run_benchmark.py                # Standalone script to regenerate benchmark cache
├── requirements.txt
├── checkpoint-25/                  # LoRA fine-tune checkpoint (Qwen2.5-1.5B, r=8, α=32)
│   ├── adapter_model.safetensors   # Trained LoRA weights
│   ├── adapter_config.json
│   └── tokenizer.json / tokenizer_config.json
├── data/
│   ├── reference_answers.json      # 50 Q&A pairs for auto-evaluation
│   ├── benchmark_cache.json        # Pre-computed benchmark results (loads on startup)
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

### 4. (Optional) Use the fine-tuned model

A trained LoRA checkpoint is included in `checkpoint-25/`. To activate it for inference:

```bash
# Merge LoRA adapter into base model and save as finetuned_model/
python -c "
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
base = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-1.5B-Instruct')
model = PeftModel.from_pretrained(base, 'checkpoint-25')
model.merge_and_unload().save_pretrained('finetuned_model')
AutoTokenizer.from_pretrained('checkpoint-25').save_pretrained('finetuned_model')
"
```

Alternatively, open `system3_finetune_colab.ipynb` in Google Colab to retrain from scratch.

### 5. Benchmark results — pre-loaded

`data/benchmark_cache.json` is included with pre-computed results for all 50 questions. The Analytics tab shows results instantly on startup. To regenerate:

```bash
python run_benchmark.py
```

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
