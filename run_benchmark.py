"""
Standalone benchmark runner — runs all 50 reference questions through
Baseline LLM and RAG, computes all 8 metrics, saves to data/benchmark_cache.json.
Run once: python run_benchmark.py
"""
import os, json, time
import numpy as np
# rouge_score MUST be imported before heavy ML libs to avoid segfault
from rouge_score import rouge_scorer as rs
from dotenv import load_dotenv

load_dotenv()

# ── Import system modules (after rouge_score) ─────────────────────────────────
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI

# ── Load reference answers ────────────────────────────────────────────────────
with open("data/reference_answers.json", encoding="utf-8") as f:
    ref_answers = json.load(f)
QUESTIONS = list(ref_answers.keys())

# ── Load vector store ─────────────────────────────────────────────────────────
INDEX_PATH = "data/faiss_index"
print("Loading vector store...")
emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vs  = FAISS.load_local(INDEX_PATH, emb, allow_dangerous_deserialization=True)
print("Vector store ready.\n")

# ── Groq client ───────────────────────────────────────────────────────────────
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
MODEL = "llama-3.1-8b-instant"

BASELINE_SYS = (
    "You are a programming tutor specializing in Data Structures, Algorithms, "
    "and Web Development. Answer questions clearly and concisely."
)
RAG_SYS = (
    "You are a programming tutor. Use only the provided context to answer. "
    "If the answer is not in the context, say 'I don't have that in my knowledge base.'"
)

def ask_baseline(q: str) -> dict:
    t = time.time()
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": BASELINE_SYS}, {"role": "user", "content": q}],
        max_tokens=300, temperature=0.3,
    )
    return {"answer": r.choices[0].message.content.strip(), "response_time": round(time.time()-t, 2)}

def ask_rag(q: str) -> dict:
    t = time.time()
    docs    = vs.similarity_search(q, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    prompt  = f"Context:\n{context}\n\nQuestion: {q}\nAnswer:"
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": RAG_SYS}, {"role": "user", "content": prompt}],
        max_tokens=300, temperature=0.3,
    )
    return {"answer": r.choices[0].message.content.strip(),
            "response_time": round(time.time()-t, 2), "context": context}

# ── Metric helpers ────────────────────────────────────────────────────────────
scorer = rs.RougeScorer(["rougeL"], use_stemmer=True)

def _cosine(a, b):
    n = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / (n + 1e-8))

def compute_metrics(answer: str, question: str, context: str = "") -> dict:
    if not answer or not answer.strip():
        return {"accuracy": 0, "rouge_l": 0, "groundedness": 0,
                "answer_relevance": 0, "faithfulness": 0}
    try:
        a_emb = np.array(vs.embeddings.embed_query(answer))
        q_emb = np.array(vs.embeddings.embed_query(question))
        answer_relevance = round(max(0.0, _cosine(a_emb, q_emb)), 3)

        ref = ref_answers.get(question.strip().lower(), "")
        accuracy, rouge_l = 0.0, 0.0
        if ref:
            rouge_l  = round(scorer.score(ref, answer)["rougeL"].fmeasure, 3)
            r_emb    = np.array(vs.embeddings.embed_query(ref))
            accuracy = round(max(0.0, _cosine(a_emb, r_emb)), 3)

        if context and context.strip():
            c_emb = np.array(vs.embeddings.embed_query(context[:1000]))
            groundedness = round(max(0.0, _cosine(a_emb, c_emb)), 3)
            faithfulness = round(scorer.score(context[:1000], answer)["rougeL"].fmeasure, 3)
        else:
            groundedness = accuracy
            faithfulness = rouge_l

        return {"accuracy": accuracy, "rouge_l": rouge_l,
                "groundedness": groundedness, "answer_relevance": answer_relevance,
                "faithfulness": faithfulness}
    except Exception as e:
        print(f"  [metric error] {e}")
        return {"accuracy": 0, "rouge_l": 0, "groundedness": 0,
                "answer_relevance": 0, "faithfulness": 0}

def _cost(answer: str, system: str) -> float:
    tokens = max(1, len(answer.split()))
    if   system == "r1": return round(0.001 + tokens * 0.0000059, 4)
    elif system == "r2": return round(0.0015 + tokens * 0.0000059 * 1.8, 4)
    else:                return round(tokens * 0.0000015, 4)

# ── Run benchmark ─────────────────────────────────────────────────────────────
# Load existing partial results to resume if interrupted
OUT_PATH = "data/benchmark_cache.json"
if os.path.exists(OUT_PATH):
    with open(OUT_PATH, encoding="utf-8") as f:
        results = json.load(f)
    done_qs = {r["question"] for r in results}
    print(f"Resuming — {len(results)} already done.\n")
else:
    results  = []
    done_qs  = set()

total = len(QUESTIONS)
print(f"Running benchmark on {total} questions...\n")

for i, q in enumerate(QUESTIONS):
    if q in done_qs:
        print(f"[{i+1:02d}/{total}] SKIP (cached): {q[:55]}")
        continue

    print(f"[{i+1:02d}/{total}] {q[:60]}")

    r1  = ask_baseline(q)
    r2  = ask_rag(q)
    ctx = r2.get("context", "")

    m1 = compute_metrics(r1["answer"], q)
    m2 = compute_metrics(r2["answer"], q, context=ctx)

    results.append({
        "question":  q,
        "r1_time":   r1["response_time"], "r2_time": r2["response_time"], "r3_time": 0,
        "r1_rouge":  m1["rouge_l"],   "r2_rouge":  m2["rouge_l"],   "r3_rouge":  0,
        "r1_sim":    m1["accuracy"],  "r2_sim":    m2["accuracy"],  "r3_sim":    0,
        "r1_ground": m1["groundedness"], "r2_ground": m2["groundedness"], "r3_ground": 0,
        "r1_relev":  m1["answer_relevance"], "r2_relev": m2["answer_relevance"], "r3_relev": 0,
        "r1_faith":  m1["faithfulness"], "r2_faith": m2["faithfulness"], "r3_faith": 0,
        "r1_cost":   _cost(r1["answer"], "r1"),
        "r2_cost":   _cost(r2["answer"], "r2"),
        "r3_cost":   0,
    })
    print(f"       r1_acc={m1['accuracy']:.2f}  r2_acc={m2['accuracy']:.2f} | "
          f"r1={r1['response_time']}s  r2={r2['response_time']}s")

    # Save after every question so we can resume if interrupted
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

# ── Summary ───────────────────────────────────────────────────────────────────
n = len(results)
r1_acc = round(sum(r["r1_sim"] for r in results) / n * 100, 1)
r2_acc = round(sum(r["r2_sim"] for r in results) / n * 100, 1)
r1_t   = round(sum(r["r1_time"] for r in results) / n, 2)
r2_t   = round(sum(r["r2_time"] for r in results) / n, 2)
print(f"\nDone! {n} rows saved to {OUT_PATH}")
print(f"  Baseline  — accuracy {r1_acc}%  avg_time {r1_t}s")
print(f"  RAG       — accuracy {r2_acc}%  avg_time {r2_t}s")
