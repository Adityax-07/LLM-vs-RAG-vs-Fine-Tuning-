"""
Fills r3_* (Fine-Tuned) metrics into existing benchmark_cache.json.
Run this ONCE after system3_inference.py is updated to use checkpoint-25/.

python fill_r3.py
"""
import os, json, time
import numpy as np

# rouge_score MUST come before any heavy ML imports
from rouge_score import rouge_scorer as rs
from dotenv import load_dotenv

load_dotenv()

# ── ML imports AFTER rouge_score ──────────────────────────────────────────────
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from system3_inference import ask_finetuned  # now points to checkpoint-25

# ── Load reference answers ────────────────────────────────────────────────────
with open("data/reference_answers.json", encoding="utf-8") as f:
    ref_answers = json.load(f)

# ── Load embeddings + vector store (for metric computation) ──────────────────
INDEX_PATH = "data/faiss_index"
print("Loading embeddings / vector store...")
emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vs  = FAISS.load_local(INDEX_PATH, emb, allow_dangerous_deserialization=True)
print("Ready.\n")

scorer = rs.RougeScorer(["rougeL"], use_stemmer=True)

def _cosine(a, b):
    n = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / (n + 1e-8))

def compute_metrics(answer: str, question: str) -> dict:
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

        # For fine-tuned: no retrieval context, so groundedness = accuracy, faithfulness = rouge_l
        return {"accuracy": accuracy, "rouge_l": rouge_l,
                "groundedness": accuracy, "answer_relevance": answer_relevance,
                "faithfulness": rouge_l}
    except Exception as e:
        print(f"  [metric error] {e}")
        return {"accuracy": 0, "rouge_l": 0, "groundedness": 0,
                "answer_relevance": 0, "faithfulness": 0}

def _cost(answer: str) -> float:
    tokens = max(1, len(answer.split()))
    return round(tokens * 0.0000015, 4)  # local model, near-zero cost

# ── Load existing cache ───────────────────────────────────────────────────────
OUT_PATH = "data/benchmark_cache.json"
with open(OUT_PATH, encoding="utf-8") as f:
    results = json.load(f)

total = len(results)
print(f"Filling r3 values for {total} cached questions...\n")
print("(Loading fine-tuned model on first question — ~30s)\n")

for i, row in enumerate(results):
    q = row["question"]
    print(f"[{i+1:02d}/{total}] {q[:65]}")

    r3 = ask_finetuned(q)
    answer = r3.get("answer", "")
    elapsed = r3.get("response_time", 0)

    m = compute_metrics(answer, q)

    row["r3_time"]   = elapsed
    row["r3_rouge"]  = m["rouge_l"]
    row["r3_sim"]    = m["accuracy"]
    row["r3_ground"] = m["groundedness"]
    row["r3_relev"]  = m["answer_relevance"]
    row["r3_faith"]  = m["faithfulness"]
    row["r3_cost"]   = _cost(answer)

    print(f"       r3_acc={m['accuracy']:.3f}  r3_rouge={m['rouge_l']:.3f}  time={elapsed}s")

    # Save after every row so we can resume on crash
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

# ── Summary ───────────────────────────────────────────────────────────────────
n = len(results)
r3_acc  = round(sum(r["r3_sim"]   for r in results) / n * 100, 1)
r3_rl   = round(sum(r["r3_rouge"] for r in results) / n, 3)
r3_t    = round(sum(r["r3_time"]  for r in results) / n, 2)
print(f"\nDone! r3 values saved to {OUT_PATH}")
print(f"  Fine-Tuned — accuracy {r3_acc}%  rouge_l {r3_rl}  avg_time {r3_t}s")
