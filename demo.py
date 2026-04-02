import os
import streamlit as st
from system1_baseline import ask_baseline
from system2_rag import ask_rag, load_vectorstore, build_vectorstore

st.set_page_config(
    page_title="CodeSage",
    page_icon="🧙",
    layout="wide"
)

# ── Session state init ────────────────────────────────────────────────────────
if "ratings" not in st.session_state:
    st.session_state.ratings = []          # list of rating dicts
if "last_results" not in st.session_state:
    st.session_state.last_results = None   # most recent answers
if "rating_submitted" not in st.session_state:
    st.session_state.rating_submitted = False

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* System 1 — Blue */
.card-blue {
    background: linear-gradient(135deg, #0d1f3c, #102a4c);
    border: 1px solid #2563eb;
    border-top: 4px solid #3b82f6;
    border-radius: 12px;
    padding: 20px;
    margin-top: 10px;
    min-height: 180px;
}
.card-blue .answer { color: #93c5fd; font-size: 15px; line-height: 1.7; }
.card-blue .time   { color: #60a5fa; font-size: 13px; margin-top: 12px; }

/* System 2 — Teal/Green */
.card-teal {
    background: linear-gradient(135deg, #052e1c, #063d24);
    border: 1px solid #059669;
    border-top: 4px solid #10b981;
    border-radius: 12px;
    padding: 20px;
    margin-top: 10px;
    min-height: 180px;
}
.card-teal .answer  { color: #6ee7b7; font-size: 15px; line-height: 1.7; }
.card-teal .time    { color: #34d399; font-size: 13px; margin-top: 12px; }
.card-teal .context { background: #063d24; border: 1px solid #065f46; border-radius: 8px;
                      padding: 12px; margin-top: 14px; color: #a7f3d0;
                      font-size: 13px; line-height: 1.6; }
.card-teal .ctx-label { color: #6ee7b7; font-size: 12px; font-weight: 600;
                         margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }

/* System 3 — Purple */
.card-purple {
    background: linear-gradient(135deg, #1a0a2e, #220d3b);
    border: 1px solid #7c3aed;
    border-top: 4px solid #8b5cf6;
    border-radius: 12px;
    padding: 20px;
    margin-top: 10px;
    min-height: 180px;
}
.card-purple .answer { color: #c4b5fd; font-size: 15px; line-height: 1.7; }
.card-purple .time   { color: #a78bfa; font-size: 13px; margin-top: 12px; }

/* Section headers */
.sys-header { font-size: 18px; font-weight: 700; margin-bottom: 2px; }
.sys-blue   { color: #3b82f6; }
.sys-teal   { color: #10b981; }
.sys-purple { color: #8b5cf6; }

/* Rating box */
.rating-box {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 18px 20px;
    margin-top: 8px;
}

/* Eval table */
.eval-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    margin-top: 10px;
}
.eval-table th {
    padding: 12px 16px;
    text-align: center;
    font-weight: 700;
    font-size: 15px;
    border-bottom: 2px solid #374151;
}
.eval-table th:first-child { text-align: left; color: #9ca3af; }
.eval-table th.col-blue   { color: #3b82f6; }
.eval-table th.col-teal   { color: #10b981; }
.eval-table th.col-purple { color: #8b5cf6; }
.eval-table td {
    padding: 11px 16px;
    text-align: center;
    border-bottom: 1px solid #1f2937;
    color: #d1d5db;
}
.eval-table td:first-child { text-align: left; color: #9ca3af; font-weight: 600; }
.eval-table tr:hover td { background: #111827; }
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 13px;
}
.badge-green  { background: #052e1c; color: #10b981; border: 1px solid #059669; }
.badge-yellow { background: #1c1a05; color: #f59e0b; border: 1px solid #d97706; }
.badge-red    { background: #2e0505; color: #ef4444; border: 1px solid #dc2626; }
.badge-grey   { background: #1f2937; color: #6b7280; border: 1px solid #374151; }
.metric-note  { color: #6b7280; font-size: 12px; font-weight: 400; }
</style>
""", unsafe_allow_html=True)

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("🧙 CODESAGE")
st.markdown(
    "**Comparative Study — RAG vs Fine-Tuning for Domain-Specific QA**  \n"
    "Ask the same question to all 3 systems and compare their answers."
)

# ── Load vector store once ────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Building knowledge base...")
def get_vectorstore():
    if not os.path.exists("data/faiss_index"):
        return build_vectorstore()
    return load_vectorstore()

vs = get_vectorstore()

# ── Input ─────────────────────────────────────────────────────────────────────
st.divider()
question = st.text_input(
    "Enter your question:",
    placeholder="e.g. What is binary search? / What are React hooks? / Explain merge sort."
)

sample_questions = [
    "What is binary search?",
    "What is the difference between stack and queue?",
    "Explain merge sort.",
    "What are React hooks?",
    "What is a REST API?",
    "What is dynamic programming?",
]

st.markdown("**Quick questions:**")
cols = st.columns(len(sample_questions))
for i, sq in enumerate(sample_questions):
    if cols[i].button(sq, key=f"sq_{i}"):
        question = sq

# ── Run systems ───────────────────────────────────────────────────────────────
if st.button("Ask All 3 Systems", type="primary") and question:
    st.session_state.rating_submitted = False  # reset for new question
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<p class="sys-header sys-blue">System 1 — Baseline LLM</p>', unsafe_allow_html=True)
        st.caption("Prompt only. No extra knowledge.")
        with st.spinner("Generating..."):
            r1 = ask_baseline(question)

    with col2:
        st.markdown('<p class="sys-header sys-teal">System 2 — RAG Chatbot</p>', unsafe_allow_html=True)
        st.caption("Retrieves from knowledge base, then generates.")
        with st.spinner("Retrieving + generating..."):
            r2 = ask_rag(question, vs)

    with col3:
        st.markdown('<p class="sys-header sys-purple">System 3 — Fine-Tuned Model</p>', unsafe_allow_html=True)
        st.caption("TinyLlama fine-tuned on programming Q&A via LoRA.")
        if os.path.exists("./finetuned_model"):
            with st.spinner("Generating..."):
                from system3_inference import ask_finetuned
                r3 = ask_finetuned(question)
        else:
            r3 = {"answer": "Model not available.", "response_time": 0}

    # persist results so they survive reruns
    st.session_state.last_results = {
        "question": question,
        "r1": r1, "r2": r2, "r3": r3,
    }

# ── Always render answers if they exist ───────────────────────────────────────
if st.session_state.last_results:
    res = st.session_state.last_results
    r1, r2, r3 = res["r1"], res["r2"], res["r3"]

    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<p class="sys-header sys-blue">System 1 — Baseline LLM</p>', unsafe_allow_html=True)
        st.caption("Prompt only. No extra knowledge.")
        st.markdown(f"""
        <div class="card-blue">
            <div class="answer">{r1['answer']}</div>
            <div class="time">⏱️ Response Time: {r1['response_time']}s</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="sys-header sys-teal">System 2 — RAG Chatbot</p>', unsafe_allow_html=True)
        st.caption("Retrieves from knowledge base, then generates.")
        st.markdown(f"""
        <div class="card-teal">
            <div class="answer">{r2['answer']}</div>
            <div class="time">⏱️ Response Time: {r2['response_time']}s</div>
            <div class="context">
                <div class="ctx-label">📄 Context retrieved from knowledge base</div>
                {r2['context_used']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown('<p class="sys-header sys-purple">System 3 — Fine-Tuned Model</p>', unsafe_allow_html=True)
        st.caption("TinyLlama fine-tuned on programming Q&A via LoRA.")
        if r3["answer"] == "Model not available.":
            st.warning(
                "Fine-tuned model not ready yet.  \n"
                "Run `system3_finetune_colab.ipynb` on Google Colab, "
                "download `finetuned_model.zip`, and unzip it here."
            )
        else:
            st.markdown(f"""
            <div class="card-purple">
                <div class="answer">{r3['answer']}</div>
                <div class="time">⏱️ Response Time: {r3['response_time']}s</div>
            </div>
            """, unsafe_allow_html=True)

# ── Rating section ─────────────────────────────────────────────────────────────
if st.session_state.last_results and not st.session_state.rating_submitted:
    st.divider()
    st.subheader("Rate the Answers")
    st.caption("Your ratings are used to build the live evaluation table below.")

    rc1, rc2, rc3 = st.columns(3)

    with rc1:
        st.markdown("**System 1 — Baseline LLM**")
        c1_correct = st.slider("Correctness (1–5)", 1, 5, 3, key="c1_correct")
        c1_halluc  = st.checkbox("Hallucination detected?", key="c1_halluc")
        c1_complete= st.slider("Completeness (1–5)", 1, 5, 3, key="c1_complete")

    with rc2:
        st.markdown("**System 2 — RAG Chatbot**")
        c2_correct = st.slider("Correctness (1–5)", 1, 5, 3, key="c2_correct")
        c2_halluc  = st.checkbox("Hallucination detected?", key="c2_halluc")
        c2_complete= st.slider("Completeness (1–5)", 1, 5, 3, key="c2_complete")

    with rc3:
        st.markdown("**System 3 — Fine-Tuned**")
        c3_correct = st.slider("Correctness (1–5)", 1, 5, 3, key="c3_correct")
        c3_halluc  = st.checkbox("Hallucination detected?", key="c3_halluc")
        c3_complete= st.slider("Completeness (1–5)", 1, 5, 3, key="c3_complete")

    if st.button("Submit Ratings", type="primary"):
        res = st.session_state.last_results
        st.session_state.ratings.append({
            "question":    res["question"],
            # correctness
            "c1_correct":  c1_correct,
            "c2_correct":  c2_correct,
            "c3_correct":  c3_correct,
            # hallucination (1 = yes, 0 = no)
            "c1_halluc":   1 if c1_halluc  else 0,
            "c2_halluc":   1 if c2_halluc  else 0,
            "c3_halluc":   1 if c3_halluc  else 0,
            # completeness
            "c1_complete": c1_complete,
            "c2_complete": c2_complete,
            "c3_complete": c3_complete,
            # response times (auto)
            "c1_time":     res["r1"]["response_time"],
            "c2_time":     res["r2"]["response_time"],
            "c3_time":     res["r3"]["response_time"],
        })
        st.session_state.rating_submitted = True
        st.success(f"Rating saved! Total questions rated: {len(st.session_state.ratings)}")
        st.rerun()

# ── Metrics table (live) ───────────────────────────────────────────────────────
st.divider()
st.subheader("Evaluation Metrics Comparison")

ratings = st.session_state.ratings
n = len(ratings)

if n == 0:
    st.caption("No ratings yet. Ask a question and rate the answers to populate this table.")

    # show placeholder dashes
    def badge(val, _n):
        return f'<span class="badge badge-grey">—</span>'
else:
    st.caption(f"Based on **{n} question(s)** rated by you. Response time is measured automatically.")

    def avg(key):
        return round(sum(r[key] for r in ratings) / n, 2)

    def pct(key):
        return round(sum(r[key] for r in ratings) / n * 100)

    def color_correct(v):
        if v >= 4.0: return "badge-green"
        if v >= 3.0: return "badge-yellow"
        return "badge-red"

    def color_halluc(v):   # lower = better
        if v <= 15:  return "badge-green"
        if v <= 30:  return "badge-yellow"
        return "badge-red"

    def color_complete(v):
        if v >= 4.0: return "badge-green"
        if v >= 3.0: return "badge-yellow"
        return "badge-red"

    def color_time(v):     # lower = better
        if v <= 1.0: return "badge-green"
        if v <= 2.0: return "badge-yellow"
        return "badge-red"

    v_c1 = avg("c1_correct");  v_c2 = avg("c2_correct");  v_c3 = avg("c3_correct")
    v_h1 = pct("c1_halluc");   v_h2 = pct("c2_halluc");   v_h3 = pct("c3_halluc")
    v_p1 = avg("c1_complete"); v_p2 = avg("c2_complete"); v_p3 = avg("c3_complete")
    v_t1 = avg("c1_time");     v_t2 = avg("c2_time");     v_t3 = avg("c3_time")

    def badge(val, cls):
        return f'<span class="badge {cls}">{val}</span>'

    row_correct  = (badge(f"{v_c1}/5", color_correct(v_c1)),
                    badge(f"{v_c2}/5", color_correct(v_c2)),
                    badge(f"{v_c3}/5", color_correct(v_c3)))
    row_halluc   = (badge(f"{v_h1}%",  color_halluc(v_h1)),
                    badge(f"{v_h2}%",  color_halluc(v_h2)),
                    badge(f"{v_h3}%",  color_halluc(v_h3)))
    row_complete = (badge(f"{v_p1}/5", color_complete(v_p1)),
                    badge(f"{v_p2}/5", color_complete(v_p2)),
                    badge(f"{v_p3}/5", color_complete(v_p3)))
    row_time     = (badge(f"{v_t1}s",  color_time(v_t1)),
                    badge(f"{v_t2}s",  color_time(v_t2)),
                    badge(f"{v_t3}s",  color_time(v_t3)))

if n == 0:
    dash = '<span class="badge badge-grey">—</span>'
    row_correct = row_halluc = row_complete = row_time = (dash, dash, dash)

st.markdown(f"""
<table class="eval-table">
  <thead>
    <tr>
      <th>Metric</th>
      <th class="col-blue">System 1<br><span style="font-weight:400;font-size:12px">Baseline LLM</span></th>
      <th class="col-teal">System 2<br><span style="font-weight:400;font-size:12px">RAG Chatbot</span></th>
      <th class="col-purple">System 3<br><span style="font-weight:400;font-size:12px">Fine-Tuned</span></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Correctness Score <span class="metric-note">(1–5, user rated)</span></td>
      <td>{row_correct[0]}</td><td>{row_correct[1]}</td><td>{row_correct[2]}</td>
    </tr>
    <tr>
      <td>Hallucination Rate <span class="metric-note">(%, user rated)</span></td>
      <td>{row_halluc[0]}</td><td>{row_halluc[1]}</td><td>{row_halluc[2]}</td>
    </tr>
    <tr>
      <td>Answer Completeness <span class="metric-note">(1–5, user rated)</span></td>
      <td>{row_complete[0]}</td><td>{row_complete[1]}</td><td>{row_complete[2]}</td>
    </tr>
    <tr>
      <td>Avg Response Time <span class="metric-note">(seconds, auto)</span></td>
      <td>{row_time[0]}</td><td>{row_time[1]}</td><td>{row_time[2]}</td>
    </tr>
  </tbody>
</table>
""", unsafe_allow_html=True)

if n > 0:
    if st.button("Clear All Ratings"):
        st.session_state.ratings = []
        st.rerun()

# ── About ──────────────────────────────────────────────────────────────────────
st.divider()
with st.expander("About CodeSage"):
    st.markdown("""
**Project:** CodeSage — Comparative Study of RAG and Fine-Tuning for Domain-Specific Question Answering
**Domain:** Programming Tutor (DSA + Web Development)

| System | Description |
|--------|-------------|
| Baseline | Llama 3.1 8B (via Groq) with only a system prompt |
| RAG | FAISS vector store + HuggingFace embeddings + Llama 3.1 8B (via Groq) |
| Fine-tuned | TinyLlama 1.1B fine-tuned via LoRA on 20 programming Q&A pairs |
""")
