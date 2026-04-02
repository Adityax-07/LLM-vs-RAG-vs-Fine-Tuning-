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
3. You see each answer, the RAG system's retrieved context, and response times.
4. You rate each answer (correctness, completeness, hallucination).
5. A live metrics table aggregates your ratings across all questions.

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
   Groq API           FAISS index      TinyLlama 1.1B
   Llama 3.1 8B    +  HuggingFace   (LoRA adapter loaded
   (prompt only)      embeddings     locally via PEFT)
                          │
                      Groq API
                      Llama 3.1 8B
                      (with context)
```

### System 1 — Baseline LLM
Sends the question directly to **Llama 3.1 8B** (via Groq) with a short system prompt. No extra knowledge. Represents what an off-the-shelf LLM can do.

### System 2 — RAG (Retrieval-Augmented Generation)
1. The question is embedded with `all-MiniLM-L6-v2` (HuggingFace Sentence Transformers).
2. Top-3 most similar chunks are retrieved from a **FAISS** vector store built from 17 hand-written `.txt` documents covering DSA topics and web dev concepts.
3. Those chunks are injected as context into the prompt sent to **Llama 3.1 8B** via Groq.

### System 3 — Fine-Tuned Model
**TinyLlama 1.1B** fine-tuned with **LoRA (Low-Rank Adaptation)** on ~20 curated programming Q&A pairs. Training is done on Google Colab (free GPU). The resulting adapter is loaded locally via the `peft` library for inference.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM inference | Groq API — `llama-3.1-8b-instant` |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector store | FAISS (CPU) via LangChain |
| Fine-tuning | HuggingFace Transformers + PEFT (LoRA) |
| Base model | TinyLlama/TinyLlama-1.1B-Chat-v1.0 |
| Training platform | Google Colab |
| Background animation | HTML5 Canvas (3D particle network via `components.html`) |

---

## How to Run

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

### 4. (Optional) Load the fine-tuned model
1. Open `system3_finetune_colab.ipynb` in Google Colab.
2. Run all cells — training takes ~10 min on a free T4 GPU.
3. Download `finetuned_model.zip` and unzip it in the project root.
4. Restart the Streamlit app — System 3 will now return real answers.

---

## Knowledge Base

The RAG system retrieves from 17 topic documents in `data/docs/`:

`binary_search` · `sorting_algorithms` · `dynamic_programming` · `graph_algorithms` · `trees` · `linked_list` · `stack_queue` · `recursion` · `backtracking` · `greedy_algorithms` · `hashing` · `string_algorithms` · `two_pointers` · `react_hooks` · `rest_api` · `javascript_promises` · `css_flexbox`

---

## Project Structure

```
├── demo.py                       # Streamlit app
├── system1_baseline.py           # Baseline LLM (Groq)
├── system2_rag.py                # RAG pipeline (FAISS + Groq)
├── system3_inference.py          # Fine-tuned model inference
├── system3_finetune_colab.ipynb  # LoRA training notebook
├── data/
│   ├── docs/                     # 17 knowledge base documents
│   ├── faiss_index/              # FAISS vector store (auto-built)
│   ├── finetune_data.jsonl       # Training data for fine-tuning
│   └── questions.csv             # Evaluation question set
├── finetuned_model/              # LoRA adapter (after training)
└── requirements.txt
```
