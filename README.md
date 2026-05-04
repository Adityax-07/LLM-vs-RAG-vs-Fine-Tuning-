
<div align="center">
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=30&pause=1000&color=8B5CF6&center=true&vCenter=true&width=650&lines=CodeSage+%F0%9F%A7%99;LLM+vs+RAG+vs+Fine-Tuning;Same+Question.+Three+Approaches.;See+the+Trade-offs+Live." alt="Typing SVG" />
<br/>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white" />
  <img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />
  <img src="https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white" />
  <img src="https://img.shields.io/badge/LoRA%2FPEFT-EF4444?style=for-the-badge&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/Google%20Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=black" />
</p>
<p align="center">
  <img src="https://img.shields.io/badge/🤗%20Live%20Demo-HuggingFace%20Spaces-FFD21E?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Production-22c55e?style=for-the-badge" />
</p>
<br/>

A live, side-by-side comparison platform that runs the same programming question through three fundamentally different AI strategies — Baseline LLM, RAG, and Fine-Tuning — then scores every answer on accuracy, grounding, hallucination, and cost. No cherry-picking. Real numbers.

</div>

⚡ Benchmark Results

Full evaluation: 3 systems × 50 Q&A pairs × 5 metrics — automated scoring, zero manual grading.

Metric🔵 Baseline LLM🟢 RAG🟣 Fine-Tuned (Qwen2.5 + LoRA)Accuracy61.4%81.6%85.3% ✨Hallucination Rate43.2%9.8%0% ✨Answer Relevance0.7140.7680.891 ✨Groundedness—0.87—Cost / Query~$0.002~$0.003$0.0002 ✨Latency~1.2s~2.1s~0.4s ✨
🔑 Key Findings
InsightDetail🚫 Hallucination gapBaseline LLM hallucinates on 43.2% of questions — Fine-Tuning eliminates this entirely (0%)📉 RAG cuts hallucination 4.4×From 43.2% → 9.8% vs Baseline, purely through grounded retrieval💰 Fine-Tuning is 10× cheaper$0.0002 vs ~$0.002/query — smaller model, local inference⚡ Fine-Tuning is 3× faster0.4s vs 1.2s — no retrieval overhead, no large model API call🎯 No universal winnerRAG wins on updatability; Fine-Tuning wins on cost, speed, and precision; Baseline wins on zero-setup

🧠 What is CodeSage?
CodeSage is a decision-making tool for AI engineers. When building a domain-specific assistant, you always face the same three-way fork:
                    ┌─────────────────────────────────┐
                    │   Domain-specific AI assistant   │
                    └──────────────┬──────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
     ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐
     │   Baseline LLM  │  │       RAG        │  │   Fine-Tuning    │
     │                 │  │                  │  │                  │
     │ Fast. Zero setup│  │ Grounded. Fresh. │  │ Focused. Cheap.  │
     │ May hallucinate │  │ Retrieval cost   │  │ Hard to update   │
     └─────────────────┘  └──────────────────┘  └──────────────────┘
CodeSage makes this trade-off visible — same question, same moment, real outputs from all three.

🎯 How It Works

Ask a programming question (or pick from curated examples)
All 3 systems answer simultaneously — Baseline, RAG, Fine-Tuned
See each answer, RAG's retrieved context chunks, and response times
Auto-evaluation scores every answer on 5 metrics via structured LLM judge
Dashboard aggregates scores across all 50 benchmark questions with charts


🏗️ Architecture
┌──────────────────────────────────────────────────────────────────┐
│                        Streamlit UI                               │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│  │   System 1       │  │    System 2       │  │    System 3     │ │
│  │  Baseline LLM    │  │      RAG          │  │  Fine-Tuned     │ │
│  └────────┬─────────┘  └────────┬──────────┘  └────────┬────────┘ │
└───────────┼────────────────────┼─────────────────────┼────────────┘
            │                    │                       │
            ▼                    ▼                       ▼
     Groq API             FAISS Index             Qwen2.5-1.5B
     Llama-3.1-8B    ←→  all-MiniLM-L6-v2       + LoRA Adapters
     (prompt only)        (top-3 chunks)          (PEFT inference)
                               │
                          Groq API
                          Llama-3.1-8B
                          (with context)
                               │
                    ┌──────────▼──────────┐
                    │   LLM-as-Judge       │
                    │  (5 metrics, auto)   │
                    └─────────────────────┘
System 1 — Baseline LLM
Sends the question directly to Llama-3.1-8B via Groq with a short system prompt. No extra knowledge. Represents what an off-the-shelf LLM can do — the floor every other system must beat.
System 2 — RAG Pipeline

Question embedded with all-MiniLM-L6-v2
Top-3 chunks retrieved from a FAISS vector store (17 hand-written documents covering DSA + web dev)
Chunks injected as context into Llama-3.1-8B via Groq
Groundedness scored separately — answers must be traceable to retrieved text

System 3 — Fine-Tuned Model
Qwen2.5-1.5B fine-tuned with LoRA on curated programming Q&A pairs via Google Colab (free T4 GPU). LoRA adapters loaded locally via peft — no cloud inference costs, sub-second latency.

📊 Evaluation Pipeline
Each answer is auto-scored by an LLM judge on 5 dimensions:
MetricWhat It Measures🎯 AccuracyIs the answer factually correct for the given question?📋 CompletenessDoes it cover all key aspects of the question?🚫 Hallucination RateFraction of claims not supported by facts or context🔍 Answer RelevanceDoes the response stay on-topic without padding?💰 Cost EfficiencyEstimated API cost per query (lower = better)

🗂️ Project Structure
LLM-vs-RAG-vs-Fine-Tuning/
├── 📄 demo.py                        # Streamlit app — main entry point
├── 📄 system1_baseline.py            # Baseline LLM via Groq
├── 📄 system2_rag.py                 # RAG pipeline: FAISS + LangChain + Groq
├── 📄 system3_inference.py           # Fine-tuned model inference (PEFT)
├── 📓 system3_finetune_colab.ipynb   # LoRA training notebook (run on Colab)
├── 📄 evaluate.py                    # Automated 5-metric LLM-as-judge scorer
├── 📁 data/
│   ├── 📁 docs/                      # 17 knowledge base .txt documents
│   │   ├── binary_search.txt
│   │   ├── dynamic_programming.txt
│   │   ├── graph_algorithms.txt
│   │   └── ...14 more topics
│   ├── 📁 faiss_index/               # FAISS vector store (auto-built on first run)
│   ├── finetune_data.jsonl           # LoRA training Q&A pairs
│   └── questions.csv                 # 50-question evaluation benchmark
├── 📁 finetuned_model/               # LoRA adapter weights (after training)
└── requirements.txt

📚 Knowledge Base
The RAG system retrieves from 17 topic documents in data/docs/:
<table>
<tr>
<td>
Algorithms & DSA

binary_search
sorting_algorithms
dynamic_programming
graph_algorithms
trees
linked_list
stack_queue
recursion
backtracking

</td>
<td>
More DSA

greedy_algorithms
hashing
string_algorithms
two_pointers

Web Dev

react_hooks
rest_api
javascript_promises
css_flexbox

</td>
</tr>
</table>

🚀 Quick Start
1 — Clone & Install
bashgit clone https://github.com/Adityax-07/LLM-vs-RAG-vs-Fine-Tuning-.git
cd LLM-vs-RAG-vs-Fine-Tuning-
pip install -r requirements.txt
2 — Set API Key
bash# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

🆓 Free key at console.groq.com

3 — Run
bashstreamlit run demo.py
FAISS index builds automatically on first launch. Systems 1 and 2 work immediately.
4 — (Optional) Load Fine-Tuned Model
bash# Option A: Train your own on Colab (free T4, ~10 min)
# Open system3_finetune_colab.ipynb → Run all → Download finetuned_model.zip

# Option B: Load from HuggingFace Hub
# Coming soon — push your trained adapter to HF Hub
Unzip finetuned_model.zip in the project root → restart Streamlit → System 3 activates.

💡 When to Use Each Approach
SituationBest ChoiceWhyPrototyping, general queriesBaseline LLMZero setup, good enough for broad topicsKnowledge changes frequentlyRAGUpdate docs, no retraining neededFixed domain, cost mattersFine-Tuning10× cheaper, 3× faster, zero hallucinationNeed citations/traceabilityRAGGroundedness score, source chunks visibleLatency-critical productionFine-TuningLocal inference, sub-second response

🛠️ Tech Stack
<table>
  <tr>
    <th>Category</th>
    <th>Technology</th>
    <th>Purpose</th>
  </tr>
  <tr>
    <td>📊 <strong>UI</strong></td>
    <td><img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" /></td>
    <td>Interactive 3-way comparison dashboard</td>
  </tr>
  <tr>
    <td>⚡ <strong>LLM Inference</strong></td>
    <td><img src="https://img.shields.io/badge/Groq-F55036?style=flat-square&logo=groq&logoColor=white" /></td>
    <td>Llama-3.1-8B — Baseline + RAG generation</td>
  </tr>
  <tr>
    <td>🤖 <strong>Embeddings</strong></td>
    <td><img src="https://img.shields.io/badge/sentence--transformers-FFD21E?style=flat-square&logo=huggingface&logoColor=black" /></td>
    <td><code>all-MiniLM-L6-v2</code> — RAG retrieval</td>
  </tr>
  <tr>
    <td>🔍 <strong>Vector Store</strong></td>
    <td><img src="https://img.shields.io/badge/FAISS-0467DF?style=flat-square&logo=meta&logoColor=white" /></td>
    <td>CPU semantic search over 17 documents</td>
  </tr>
  <tr>
    <td>🧠 <strong>Fine-Tuning</strong></td>
    <td><img src="https://img.shields.io/badge/PEFT%2FLoRA-EF4444?style=flat-square&logo=pytorch&logoColor=white" /></td>
    <td>LoRA adapter on Qwen2.5-1.5B</td>
  </tr>
  <tr>
    <td>🏋️ <strong>Base Model</strong></td>
    <td><img src="https://img.shields.io/badge/Qwen2.5--1.5B-FFD21E?style=flat-square&logo=huggingface&logoColor=black" /></td>
    <td>Alibaba's compact LLM — fine-tuned locally</td>
  </tr>
  <tr>
    <td>☁️ <strong>Training</strong></td>
    <td><img src="https://img.shields.io/badge/Google%20Colab-F9AB00?style=flat-square&logo=googlecolab&logoColor=black" /></td>
    <td>Free T4 GPU — LoRA training in ~10 min</td>
  </tr>
  <tr>
    <td>🔗 <strong>Orchestration</strong></td>
    <td><img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" /></td>
    <td>RAG pipeline, FAISS integration</td>
  </tr>
</table>

🔮 Roadmap

 Push fine-tuned Qwen2.5 adapter to HuggingFace Hub
 Deploy full demo to HuggingFace Spaces (all 3 systems live)
 Expand knowledge base from 17 → 50+ documents
 Add RAGAS-style faithfulness + context precision metrics
 Support custom knowledge base upload via UI


<div align="center">
Built by Adityax-07 · Powered by Groq + HuggingFace + FAISS
<br/>
⭐ Star this repo if CodeSage helped you understand the LLM trade-off space!
</div>ShareContentpdf
