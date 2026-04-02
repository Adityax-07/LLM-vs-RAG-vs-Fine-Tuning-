"""
Runs all 3 systems on the test questions and saves results to results/evaluation_results.csv.
After running, open the CSV and manually fill in:
  - correctness_score (1-5): 1=wrong, 3=partial, 5=perfect
  - hallucination (Yes/No): Yes if the answer contains false information
"""
import csv
import os
import time

from system1_baseline import ask_baseline
from system2_rag import ask_rag, load_vectorstore, build_vectorstore

QUESTIONS_PATH = "data/questions.csv"
RESULTS_PATH = "results/evaluation_results.csv"
NUM_QUESTIONS = 30  # increase to 50 when ready


def load_questions():
    questions = []
    with open(QUESTIONS_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row["question"])
    return questions[:NUM_QUESTIONS]


def run_evaluation():
    os.makedirs("results", exist_ok=True)

    # Load RAG vectorstore
    if not os.path.exists("data/faiss_index"):
        print("Building FAISS index first...")
        vs = build_vectorstore()
    else:
        print("Loading existing FAISS index...")
        vs = load_vectorstore()

    questions = load_questions()
    print(f"\nEvaluating {len(questions)} questions across 3 systems...\n")

    results = []

    for i, q in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] {q}")

        r1 = ask_baseline(q)
        time.sleep(0.5)  # avoid rate limiting
        r2 = ask_rag(q, vs)
        time.sleep(0.5)

        # System 3 — placeholder until fine-tuned model is ready
        try:
            from system3_inference import ask_finetuned
            r3 = ask_finetuned(q)
        except Exception:
            r3 = {"answer": "Model not available yet.", "response_time": 0}

        results.append({
            "id": i,
            "question": q,
            # Baseline
            "baseline_answer": r1["answer"],
            "baseline_time": r1["response_time"],
            "baseline_correctness": "",   # Fill manually: 1-5
            "baseline_hallucination": "", # Fill manually: Yes/No
            # RAG
            "rag_answer": r2["answer"],
            "rag_time": r2["response_time"],
            "rag_correctness": "",
            "rag_hallucination": "",
            # Fine-tuned
            "finetuned_answer": r3["answer"],
            "finetuned_time": r3["response_time"],
            "finetuned_correctness": "",
            "finetuned_hallucination": "",
        })

        print(f"  Baseline ({r1['response_time']}s): {r1['answer'][:70]}...")
        print(f"  RAG      ({r2['response_time']}s): {r2['answer'][:70]}...")
        print()

    # Save CSV
    with open(RESULTS_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved {len(results)} results to {RESULTS_PATH}")
    print("\nNext step: open the CSV and fill in 'correctness' (1-5) and 'hallucination' (Yes/No) columns manually.")


def print_summary():
    """Print average scores after you have manually filled in the CSV."""
    if not os.path.exists(RESULTS_PATH):
        print("No results file found. Run evaluate.py first.")
        return

    baseline_scores, rag_scores, ft_scores = [], [], []
    baseline_hall, rag_hall, ft_hall = [], [], []
    baseline_times, rag_times, ft_times = [], [], []

    with open(RESULTS_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["baseline_correctness"]:
                baseline_scores.append(float(row["baseline_correctness"]))
                baseline_hall.append(1 if row["baseline_hallucination"].strip().lower() == "yes" else 0)
                baseline_times.append(float(row["baseline_time"]) if row["baseline_time"] else 0)
            if row["rag_correctness"]:
                rag_scores.append(float(row["rag_correctness"]))
                rag_hall.append(1 if row["rag_hallucination"].strip().lower() == "yes" else 0)
                rag_times.append(float(row["rag_time"]) if row["rag_time"] else 0)
            if row["finetuned_correctness"]:
                ft_scores.append(float(row["finetuned_correctness"]))
                ft_hall.append(1 if row["finetuned_hallucination"].strip().lower() == "yes" else 0)
                ft_times.append(float(row["finetuned_time"]) if row["finetuned_time"] else 0)

    def avg(lst): return round(sum(lst) / len(lst), 2) if lst else "N/A"
    def pct(lst): return f"{round(sum(lst)/len(lst)*100)}%" if lst else "N/A"

    print("\n===== EVALUATION SUMMARY =====")
    print(f"{'Metric':<30} {'Baseline':>12} {'RAG':>12} {'Fine-tuned':>12}")
    print("-" * 66)
    print(f"{'Avg Correctness (1-5)':<30} {avg(baseline_scores):>12} {avg(rag_scores):>12} {avg(ft_scores):>12}")
    print(f"{'Hallucination Rate':<30} {pct(baseline_hall):>12} {pct(rag_hall):>12} {pct(ft_hall):>12}")
    print(f"{'Avg Response Time (s)':<30} {avg(baseline_times):>12} {avg(rag_times):>12} {avg(ft_times):>12}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        print_summary()
    else:
        run_evaluation()
