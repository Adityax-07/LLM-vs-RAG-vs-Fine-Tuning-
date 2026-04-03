

# 🧙 CodeSage

**A comparative study of three LLM strategies for domain-specific question answering.**

CodeSage puts a Baseline LLM, a RAG pipeline, and a Fine-Tuned model side-by-side so you can ask the same programming question and immediately see how each approach differs in accuracy, grounding, and speed.

---

## Why This Project?

When building an AI assistant for a specific domain (here: programming / DSA / web dev), you have three realistic options:

| Approach | Core idea | Trade-off |
|---|---|---|
| **Baseline LLM** | Prompt a large general-purpose model | Fast, zero setup — but may hallucinate or give vague answers |
| **RAG** | Retrieve relevant docs first, then generate | Grounded answers, updatable knowledge — retrieval adds latency |
| **Fine-Tuning** | Train a smaller model on domain data | Potentially fastest, very focused — expensive to update |

There is no universal winner. The goal of CodeSage is to **make that trade-off visible** with real side-by-side outputs and user-rated metrics.

---

## What It Does

1. You type (or click) a programming question.
2. All three systems answer it simultaneously.
3. Each answer shows auto-computed **ROUGE-L** and **semantic similarity** scores against a reference answer.
4. You rate each answer (correctness, completeness, hallucination).
5. A live metrics table and **Plotly bar charts** aggregate your ratings across all questions.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Streamlit UI                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │  System 1    │  │  System 2    │  │ System 3  │  │
│  │  Baseline    │  │    RAG       │  │ Fine-Tuned│  │
│  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘  │
└─────────┼─────────────────┼────────────────┼─────────┘
          │                 │                │
          ▼                 ▼                ▼
   Groq API           FAISS index      Qwen2.5-1.5B
   Llama 3.1 8B    +  HuggingFace   (LoRA adapter loaded
   (prompt only)      embeddings     locally via PEFT)
                          │
                      Groq API
                      Llama 3.1 8B
                      (with context)
```

### System 1 — Baseline LLM
Sends the question directly to **Llama 3.1 8B** (via Groq) with a short system prompt. No extra knowledge.

### System 2 — RAG (Retrieval-Augmented Generation)
1. The question is embedded with `all-MiniLM-L6-v2` (HuggingFace Sentence Transformers).
2. Top-3 most similar chunks are retrieved from a **FAISS** vector store built from 22 documents (`.txt` files + any PDFs dropped into `data/pdfs/`).
3. Those chunks are injected as context into the prompt sent to **Llama 3.1 8B** via Groq.

### System 3 — Fine-Tuned Model
**Qwen2.5-1.5B-Instruct** fine-tuned with **LoRA** on ~20 curated programming Q&A pairs. Training is done on Google Colab (free GPU). The adapter is loaded locally via `peft`.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM inference | Groq API — `llama-3.1-8b-instant` |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector store | FAISS (CPU) via LangChain |
| Fine-tuning | HuggingFace Transformers + PEFT (LoRA) |
| Base model | Qwen/Qwen2.5-1.5B-Instruct |
| Auto metrics | ROUGE-L (`rouge-score`) + cosine semantic similarity |
| Charts | Plotly |
| Training platform | Google Colab |
| Background animation | HTML5 Canvas 3D particle network |

---

## Deploy to HuggingFace Spaces

1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space) — SDK: **Streamlit**
2. Push this repo to the Space:
   ```bash
   git remote add space https://huggingface.co/spaces/YOUR_USERNAME/codesage
   git push space main
   ```
3. Add your `GROQ_API_KEY` as a Space secret (Settings → Variables and secrets)
4. The app launches automatically — the FAISS index is built on first run (~30s)

> System 3 (fine-tuned) will show "model unavailable" on Spaces unless you upload the `finetuned_model/` adapter folder to the Space repo.

---

## How to Run Locally

### 1. Clone & install
```bash
git clone https://github.com/Adityax-07/LLM-vs-RAG-vs-Fine-Tuning-.git
cd LLM-vs-RAG-vs-Fine-Tuning-
pip install -r requirements.txt
```

### 2. Set your Groq API key
Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com).

### 3. Run the app
```bash
streamlit run demo.py
```
The FAISS index is built automatically on first launch.

### 4. (Optional) Expand the knowledge base with PDFs
Drop any `.pdf` files into `data/pdfs/`, then delete `data/faiss_index/` and restart — PDFs are ingested automatically.

### 5. (Optional) Load the fine-tuned model
1. Open `system3_finetune_colab.ipynb` in Google Colab.
2. Run all cells — trains **Qwen2.5-1.5B-Instruct** with LoRA, takes ~15 min on a free T4 GPU.
3. Download `finetuned_model.zip` and unzip it in the project root.
4. Restart the app — System 3 returns real answers.

---

## Knowledge Base

The RAG system retrieves from 22 documents in `data/docs/`:

`binary_search` · `sorting_algorithms` · `dynamic_programming` · `graph_algorithms` · `trees` · `linked_list` · `stack_queue` · `recursion` · `backtracking` · `greedy_algorithms` · `hashing` · `string_algorithms` · `two_pointers` · `react_hooks` · `rest_api` · `javascript_promises` · `css_flexbox` · `big_o_notation` · `heaps` · `sql_basics` · `typescript_basics` · `git_basics`

Plus any PDFs placed in `data/pdfs/`.

---

## Project Structure

```
├── demo.py                       # Streamlit app
├── system1_baseline.py           # Baseline LLM (Groq)
├── system2_rag.py                # RAG pipeline (FAISS + PDF support + Groq)
├── system3_inference.py          # Fine-tuned model inference (Qwen2.5-1.5B)
├── system3_finetune_colab.ipynb  # LoRA training notebook
├── data/
│   ├── docs/                     # 22 knowledge base documents (.txt)
│   ├── pdfs/                     # Drop PDFs here to expand the knowledge base
│   ├── faiss_index/              # FAISS vector store (auto-built)
│   ├── reference_answers.json    # Reference answers for ROUGE-L / semantic similarity
│   ├── finetune_data.jsonl       # Training data for fine-tuning
│   └── questions.csv             # Evaluation question set
├── finetuned_model/              # LoRA adapter (after training)
└── requirements.txt
```
