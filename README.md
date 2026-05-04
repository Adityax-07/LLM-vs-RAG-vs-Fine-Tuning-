<div align="center">

<!-- Animated Banner -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=CodeSage%20🧙&fontSize=60&fontColor=fff&animation=twinkling&fontAlignY=35&desc=LLM%20vs%20RAG%20vs%20Fine-Tuning%20—%20Live%20Trade-off%20Platform&descAlignY=60&descSize=18" />

<!-- Typing SVG -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=22&pause=1200&color=A78BFA&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=60&lines=Same+Question.+Three+Architectures.+Real+Numbers." alt="Typing SVG" />

<br/>

<!-- Primary Badges -->
<p align="center">
  <a href="https://github.com/Adityax-07/LLM-vs-RAG-vs-Fine-Tuning-/stargazers">
    <img src="https://img.shields.io/github/stars/Adityax-07/LLM-vs-RAG-vs-Fine-Tuning-?style=for-the-badge&logo=starship&color=f59e0b&logoColor=white&labelColor=1a1a2e" />
  </a>
  <a href="https://github.com/Adityax-07/LLM-vs-RAG-vs-Fine-Tuning-/network/members">
    <img src="https://img.shields.io/github/forks/Adityax-07/LLM-vs-RAG-vs-Fine-Tuning-?style=for-the-badge&logo=git&color=8b5cf6&logoColor=white&labelColor=1a1a2e" />
  </a>
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge&logo=opensourceinitiative&logoColor=white&labelColor=1a1a2e" />
  <img src="https://img.shields.io/badge/Status-Production%20Ready-22c55e?style=for-the-badge&logo=checkmarx&logoColor=white&labelColor=1a1a2e" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e" />
</p>

<!-- Tech Stack Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq_API-F55036?style=for-the-badge&logo=groq&logoColor=white" />
  <img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />
  <img src="https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white" />
  <img src="https://img.shields.io/badge/LoRA%2FPEFT-EF4444?style=for-the-badge&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Google_Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=black" />
</p>

<!-- Skill Icons -->
<p align="center">
  <img src="https://skillicons.dev/icons?i=python,pytorch,tensorflow,git,github,vscode&theme=dark" />
</p>

<br/>

<blockquote>
🧪 <strong>CodeSage</strong> is a live, side-by-side AI research platform that fires the same programming question at three fundamentally different architectures — <strong>Baseline LLM</strong>, <strong>RAG</strong>, and <strong>Fine-Tuning</strong> — then auto-scores every answer on accuracy, hallucination, groundedness, relevance, and cost.<br/><br/>
No cherry-picking. No manual grading. <strong>Real numbers, real trade-offs.</strong>
</blockquote>

<br/>

<!-- Quick stats strip -->
<p align="center">
  <img src="https://img.shields.io/badge/50-Benchmark%20Questions-8b5cf6?style=flat-square" />
  <img src="https://img.shields.io/badge/3-AI%20Systems%20Compared-06b6d4?style=flat-square" />
  <img src="https://img.shields.io/badge/8-Auto%20Eval%20Metrics-f59e0b?style=flat-square" />
  <img src="https://img.shields.io/badge/85.3%25-Fine--Tune%20Accuracy-22c55e?style=flat-square" />
  <img src="https://img.shields.io/badge/0%25-Hallucination%20Rate-ef4444?style=flat-square" />
</p>

</div>

---

## 📌 Table of Contents

| | Section |
|:---:|:---|
| ⚡ | [Benchmark Results](#-benchmark-results) |
| 🧠 | [What is CodeSage?](#-what-is-codesage) |
| ✨ | [Features](#-features) |
| 🏗️ | [Architecture](#️-architecture) |
| 📊 | [Evaluation Pipeline](#-evaluation-pipeline) |
| 🚀 | [Quick Start](#-quick-start) |
| 📚 | [Knowledge Base](#-knowledge-base) |
| 💡 | [Decision Guide](#-decision-guide) |
| 🛠️ | [Tech Stack](#️-tech-stack) |
| 🗂️ | [Project Structure](#️-project-structure) |
| 🔮 | [Roadmap](#-roadmap) |

---

## ⚡ Benchmark Results

> **Full evaluation:** `3 systems` × `50 Q&A pairs` × `8 metrics` — fully automated, zero manual grading

| 📏 Metric | 🔵 Baseline LLM | 🟢 RAG Chatbot | 🟣 Fine-Tuned (Qwen2.5 + LoRA) |
|:---|:---:|:---:|:---:|
| 🎯 **Answer Accuracy** | 61.4% | 81.6% | **85.3% ✨** |
| 🚫 **Hallucination Rate** | 43.2% ❌ | 9.8% | **0.0% ✨** |
| 🔍 **Answer Relevance** | 0.714 | 0.768 | **0.891 ✨** |
| 📌 **Groundedness** | — | **0.87 ✨** | — |
| ⚡ **Avg Latency** | ~1.2s | ~2.1s | **~0.4s ✨** |
| 💰 **Cost / Query** | ~$0.0020 | ~$0.0030 | **$0.0002 ✨** |

### 🔑 Key Findings

| Insight | Detail |
|:---|:---|
| 🚫 **Hallucination gap** | Baseline hallucinates on `43.2%` of questions — Fine-Tuning eliminates this entirely → `0%` |
| 📉 **RAG cuts hallucination 4.4×** | From `43.2%` → `9.8%` purely through grounded retrieval, no retraining needed |
| 💰 **Fine-Tuning is 10× cheaper** | `$0.0002` vs `~$0.002` per query — smaller model, fully local inference |
| ⚡ **Fine-Tuning is 3× faster** | `0.4s` vs `1.2s` — no retrieval pipeline, no large-model API round-trip |
| 🎯 **No universal winner** | RAG wins on updatability · Fine-Tuning wins on cost/speed/precision · Baseline wins on zero-setup |

---

## 🧠 What is CodeSage?

CodeSage is a **decision-making tool** for AI engineers. When building a domain-specific assistant, you always hit the same three-way fork:

```
                       ┌──────────────────────────────────────┐
                       │     Domain-Specific AI Assistant      │
                       └─────────────────┬────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              ▼                          ▼                          ▼
   ┌──────────────────┐      ┌───────────────────┐      ┌───────────────────┐
   │  🔵 BASELINE LLM │      │  🟢 RAG PIPELINE  │      │  🟣 FINE-TUNING   │
   │                  │      │                   │      │                   │
   │  ✅ Zero setup   │      │  ✅ Always fresh  │      │  ✅ 10× cheaper   │
   │  ✅ Broad topics │      │  ✅ Grounded      │      │  ✅ 0% hallucin.  │
   │  ❌ Hallucinates │      │  ⚠️  Retrieval lag │      │  ❌ Hard to update│
   └──────────────────┘      └───────────────────┘      └───────────────────┘
```

> CodeSage makes this trade-off **visible and measurable** — same question, same moment, real output from all three.

---

## ✨ Features

<div align="center">
<table>
  <tr>
    <td align="center" width="220">
      <strong>🔀 Side-by-Side Compare</strong><br/><br/>
      Three answers to one question,<br/>simultaneously, in one view
    </td>
    <td align="center" width="220">
      <strong>📊 Auto Evaluation</strong><br/><br/>
      8-metric LLM-as-Judge scores<br/>every response automatically
    </td>
    <td align="center" width="220">
      <strong>🏆 Winner Badge</strong><br/><br/>
      Best answer highlighted;<br/>hallucination flag raised on low-confidence
    </td>
  </tr>
  <tr>
    <td align="center">
      <strong>📈 Analytics Dashboard</strong><br/><br/>
      Plotly charts + paper-style TABLE II<br/>aggregated over 50 benchmarks
    </td>
    <td align="center">
      <strong>💾 Persistent Cache</strong><br/><br/>
      Results stored in <code>benchmark_cache.json</code><br/>— instant reload, no re-running
    </td>
    <td align="center">
      <strong>📄 PDF Ingestion</strong><br/><br/>
      Drop any PDF into <code>data/pdfs/</code><br/>— RAG ingests it automatically
    </td>
  </tr>
</table>
</div>

---

## 🏗️ Architecture

```
╔══════════════════════════════════════════════════════════════════════════╗
║                           🖥️  Streamlit UI                               ║
║  ┌──────────────────┐   ┌──────────────────────┐   ┌──────────────────┐ ║
║  │  ⚡ System 1      │   │   🔍 System 2         │   │  🧠 System 3     │ ║
║  │  Baseline LLM    │   │   RAG Pipeline        │   │  Fine-Tuned      │ ║
║  └────────┬─────────┘   └──────────┬────────────┘   └────────┬─────────┘ ║
╚═══════════╪═══════════════════════╪════════════════════════╪═════════════╝
            │                       │                         │
            ▼                       ▼                         ▼
     ┌─────────────┐       ┌──────────────────┐      ┌───────────────────┐
     │  Groq API   │       │   FAISS Index    │      │  Qwen2.5-1.5B     │
     │ Llama-3.1-8B│       │ all-MiniLM-L6-v2 │      │  + LoRA Adapters  │
     │ (zero-shot) │       │  (top-3 chunks)  │      │  (PEFT, local)    │
     └─────────────┘       └────────┬─────────┘      └───────────────────┘
                                    │
                             Groq API (with context)
                                    │
                          ┌─────────▼──────────┐
                          │   🏛️  LLM-as-Judge  │
                          │  8 metrics, auto    │
                          └────────────────────┘
```

### ⚡ System 1 — Baseline LLM

Sends the question directly to **Llama-3.1-8B** via Groq with a minimal system prompt. No extra knowledge. Represents what an off-the-shelf LLM can do — the floor every other system must beat.

### 🔍 System 2 — RAG Pipeline

1. Question → `all-MiniLM-L6-v2` embedding
2. Top-3 chunks retrieved from **FAISS** vector store (17 documents)
3. Chunks injected as context into **Llama-3.1-8B** via Groq
4. Groundedness scored — answers must be traceable to retrieved text

### 🧠 System 3 — Fine-Tuned Model

**Qwen2.5-1.5B** fine-tuned with **LoRA** (`r=8, α=32`) on curated CS Q&A pairs via Google Colab T4 GPU. Adapters loaded locally via `peft` — zero cloud inference cost, sub-second latency.

---

## 📊 Evaluation Pipeline

Each answer is auto-scored by an LLM judge across **8 dimensions**:

| Icon | Metric | Description | Unit |
|:---:|:---|:---|:---:|
| 🎯 | **Answer Accuracy** | Cosine similarity of answer vs reference embedding | % |
| 📌 | **Groundedness** | Cosine similarity of answer vs retrieved context | 0–1 |
| 🚫 | **Hallucination Rate** | % of answers with accuracy < 0.5 | % |
| 🔍 | **Answer Relevance** | Cosine similarity of answer vs question | 0–1 |
| 📜 | **Faithfulness (ROUGE-L)** | Token overlap with source context or reference | 0–1 |
| ⏱️ | **Avg Response Time** | Mean latency per query | sec |
| 💰 | **Cost per Query** | Token-count-based cost estimate | USD |
| ⭐ | **Overall Score** | 30% Acc + 20% Ground + 20% (1−HR) + 15% Rel + 15% Faith | 1–5 |

---

## 🚀 Quick Start

### `Step 1` — Clone & Install

```bash
git clone https://github.com/Adityax-07/LLM-vs-RAG-vs-Fine-Tuning-.git
cd LLM-vs-RAG-vs-Fine-Tuning-
pip install -r requirements.txt
```

### `Step 2` — Configure API Key

```bash
echo "GROQ_API_KEY=your_key_here" > .env
```

> 🆓 Free key at [console.groq.com](https://console.groq.com)

### `Step 3` — Launch

```bash
streamlit run demo.py
```

> FAISS vector store builds automatically on first launch. **Systems 1 & 2 are ready instantly.**

### `Step 4` — (Optional) Activate Fine-Tuned Model

```bash
python -c "
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
base = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-1.5B-Instruct')
model = PeftModel.from_pretrained(base, 'checkpoint-25')
model.merge_and_unload().save_pretrained('finetuned_model')
AutoTokenizer.from_pretrained('checkpoint-25').save_pretrained('finetuned_model')
"
```

> Or open `system3_finetune_colab.ipynb` in **Google Colab** to train from scratch on a free T4 GPU (~10 min).

### `Step 5` — Regenerate Benchmark *(optional)*

```bash
# Pre-computed results already included in data/benchmark_cache.json
python run_benchmark.py
```

---

## 📚 Knowledge Base

The RAG system retrieves from **17 hand-crafted topic documents** in `data/docs/`:

<div align="center">
<table>
  <tr>
    <td valign="top" width="33%">
      <strong>🧮 Algorithms &amp; DSA</strong><br/><br/>
      <code>binary_search</code><br/>
      <code>sorting_algorithms</code><br/>
      <code>dynamic_programming</code><br/>
      <code>graph_algorithms</code><br/>
      <code>trees</code><br/>
      <code>linked_list</code><br/>
      <code>stack_queue</code><br/>
      <code>recursion</code><br/>
      <code>backtracking</code>
    </td>
    <td valign="top" width="33%">
      <strong>📐 More DSA</strong><br/><br/>
      <code>greedy_algorithms</code><br/>
      <code>hashing</code><br/>
      <code>string_algorithms</code><br/>
      <code>two_pointers</code><br/>
      <code>big_o_notation</code><br/>
      <code>heaps</code>
    </td>
    <td valign="top" width="33%">
      <strong>🌐 Web &amp; Tooling</strong><br/><br/>
      <code>react_hooks</code><br/>
      <code>rest_api</code><br/>
      <code>javascript_promises</code><br/>
      <code>css_flexbox</code><br/>
      <code>typescript_basics</code><br/>
      <code>sql_basics</code><br/>
      <code>git_basics</code>
    </td>
  </tr>
</table>
</div>

---

## 💡 Decision Guide

| 🤔 Situation | ✅ Best Choice | 📝 Why |
|:---|:---:|:---|
| Prototyping or general queries | **Baseline LLM** | Zero setup, covers broad topics well |
| Knowledge changes frequently | **RAG** | Update docs without retraining |
| Fixed domain, cost/latency matters | **Fine-Tuning** | 10× cheaper, 3× faster, 0% hallucination |
| Need citations & traceability | **RAG** | Groundedness score + visible source chunks |
| Production with tight latency SLA | **Fine-Tuning** | Local inference, no API round-trip |

---

## 🛠️ Tech Stack

<div align="center">
<table>
  <tr>
    <th>Layer</th>
    <th>Technology</th>
    <th>Purpose</th>
  </tr>
  <tr>
    <td>📊 <strong>UI</strong></td>
    <td>
      <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />
      <img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white" />
    </td>
    <td>3-way comparison dashboard + analytics charts</td>
  </tr>
  <tr>
    <td>⚡ <strong>LLM</strong></td>
    <td><img src="https://img.shields.io/badge/Groq_API-F55036?style=flat-square&logo=groq&logoColor=white" /></td>
    <td>Llama-3.1-8B — Baseline + RAG generation</td>
  </tr>
  <tr>
    <td>🤖 <strong>Embeddings</strong></td>
    <td><img src="https://img.shields.io/badge/sentence--transformers-FFD21E?style=flat-square&logo=huggingface&logoColor=black" /></td>
    <td><code>all-MiniLM-L6-v2</code> — RAG semantic retrieval</td>
  </tr>
  <tr>
    <td>🔍 <strong>Vector DB</strong></td>
    <td><img src="https://img.shields.io/badge/FAISS-0467DF?style=flat-square&logo=meta&logoColor=white" /></td>
    <td>CPU-based semantic search over knowledge base</td>
  </tr>
  <tr>
    <td>🧠 <strong>Fine-Tuning</strong></td>
    <td>
      <img src="https://img.shields.io/badge/PEFT%2FLoRA-EF4444?style=flat-square&logo=pytorch&logoColor=white" />
      <img src="https://img.shields.io/badge/Transformers-FFD21E?style=flat-square&logo=huggingface&logoColor=black" />
    </td>
    <td>LoRA adapter (r=8, α=32) on Qwen2.5-1.5B</td>
  </tr>
  <tr>
    <td>🏋️ <strong>Base Model</strong></td>
    <td><img src="https://img.shields.io/badge/Qwen2.5--1.5B-FFD21E?style=flat-square&logo=huggingface&logoColor=black" /></td>
    <td>Alibaba's compact LLM — LoRA fine-tuned locally</td>
  </tr>
  <tr>
    <td>☁️ <strong>Training</strong></td>
    <td><img src="https://img.shields.io/badge/Google_Colab-F9AB00?style=flat-square&logo=googlecolab&logoColor=black" /></td>
    <td>Free T4 GPU — LoRA training in ~10 minutes</td>
  </tr>
  <tr>
    <td>🔗 <strong>Orchestration</strong></td>
    <td><img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" /></td>
    <td>RAG pipeline, FAISS integration, PDF ingestion</td>
  </tr>
  <tr>
    <td>📏 <strong>Metrics</strong></td>
    <td><img src="https://img.shields.io/badge/rouge--score-EF4444?style=flat-square&logo=python&logoColor=white" /></td>
    <td>ROUGE-L + cosine similarity for auto-evaluation</td>
  </tr>
</table>
</div>

---

## 🗂️ Project Structure

```
📦 LLM-vs-RAG-vs-Fine-Tuning/
│
├── 📄 demo.py                         ← Streamlit app (main entry point)
├── 📄 system1_baseline.py             ← Baseline LLM via Groq API
├── 📄 system2_rag.py                  ← RAG pipeline: FAISS + LangChain + Groq
├── 📄 system3_inference.py            ← Fine-tuned model inference (PEFT)
├── 📓 system3_finetune_colab.ipynb    ← LoRA training notebook (Colab T4)
├── 📄 evaluate.py                     ← Standalone evaluation script
├── 📄 run_benchmark.py                ← Regenerates benchmark_cache.json
│
├── 📁 checkpoint-25/                  ← Trained LoRA weights (included)
│   ├── adapter_model.safetensors
│   ├── adapter_config.json            ← r=8, alpha=32
│   └── tokenizer.json
│
├── 📁 finetuned_model/                ← Merged model (after merge step)
│
├── 📁 data/
│   ├── 📁 docs/                       ← 17 knowledge base .txt files
│   ├── 📁 faiss_index/                ← FAISS vector store (auto-built)
│   ├── 📁 pdfs/                       ← Drop PDFs here for RAG ingestion
│   ├── benchmark_cache.json           ← Pre-computed 50Q benchmark results
│   ├── reference_answers.json         ← Ground-truth Q&A pairs
│   └── finetune_data.jsonl            ← LoRA training data (ChatML format)
│
└── 📄 requirements.txt
```

---

## 🔮 Roadmap

| Status | Feature |
|:---:|:---|
| ✅ | 50-question auto-benchmark with persistent cache |
| ✅ | LoRA fine-tune checkpoint (`checkpoint-25`) included |
| ✅ | Analytics dashboard with Plotly + TABLE II |
| ✅ | PDF ingestion into RAG knowledge base |
| 🔜 | Push Qwen2.5 LoRA adapter to HuggingFace Hub |
| 🔜 | Full 3-system live demo on HuggingFace Spaces |
| 🔜 | Expand knowledge base: 17 → 50+ documents |
| 🔜 | RAGAS-style faithfulness + context precision metrics |
| 🔜 | Custom knowledge base upload via Streamlit UI |

---

<!-- Wave footer -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer" />

<div align="center">

<strong>Built with 🧠 by <a href="https://github.com/Adityax-07">Adityax-07</a></strong>

<br/>

<em>Powered by Groq · HuggingFace · FAISS · LangChain · Streamlit</em>

<br/><br/>

<a href="https://github.com/Adityax-07">
  <img src="https://img.shields.io/badge/GitHub-Adityax--07-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>

<br/><br/>

⭐ <strong>If CodeSage helped you understand the LLM trade-off space, drop a star!</strong>

</div>
