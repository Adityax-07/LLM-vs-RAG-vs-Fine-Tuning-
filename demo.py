import os
import html as html_lib
import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from system1_baseline import ask_baseline
from system2_rag import ask_rag, load_vectorstore, build_vectorstore

st.set_page_config(
    page_title="CodeSage",
    page_icon="🧙",
    layout="wide"
)

# ── Session state ─────────────────────────────────────────────────────────────
if "ratings"          not in st.session_state: st.session_state.ratings          = []
if "last_results"     not in st.session_state: st.session_state.last_results     = None
if "rating_submitted" not in st.session_state: st.session_state.rating_submitted = False
if "input_question"   not in st.session_state: st.session_state.input_question   = ""
if "auto_run"         not in st.session_state: st.session_state.auto_run         = False
if "auto_metrics"      not in st.session_state: st.session_state.auto_metrics      = {}
if "benchmark_results" not in st.session_state: st.session_state.benchmark_results = []
if "winner"            not in st.session_state: st.session_state.winner            = None
if "halluc_flags"      not in st.session_state: st.session_state.halluc_flags      = {}

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""<style>

/* ── Global & chrome ────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
.stApp {
    background: #060b18;
    background-image:
        radial-gradient(ellipse 60% 50% at 15% 25%, rgba(59,130,246,.07) 0%, transparent 70%),
        radial-gradient(ellipse 50% 60% at 85% 75%, rgba(139,92,246,.07) 0%, transparent 70%),
        radial-gradient(ellipse 40% 40% at 50% 50%, rgba(16,185,129,.04) 0%, transparent 70%);
    animation: bgPulse 12s ease-in-out infinite alternate;
}
@keyframes bgPulse {
    0%   { background-size: 100% 100%, 100% 100%, 100% 100%; }
    100% { background-size: 120% 120%, 115% 115%, 110% 110%; }
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1400px;
}

/* ── Hero ───────────────────────────────────────────────────── */
.hero { text-align: center; padding: 2rem 1rem 0.8rem; }
.hero-eyebrow {
    font-size: 10px; font-weight: 700; letter-spacing: 3.5px;
    text-transform: uppercase; color: #334155; margin-bottom: 20px;
}

/* Animated logo icon */
.logo-wrap {
    position: relative; width: 92px; height: 92px;
    margin: 0 auto 22px;
    animation: logoFloat 4s ease-in-out infinite;
}
@keyframes logoFloat {
    0%, 100% { transform: translateY(0px); filter: drop-shadow(0 0 18px rgba(99,102,241,.35)); }
    50%       { transform: translateY(-9px); filter: drop-shadow(0 0 28px rgba(99,102,241,.55)); }
}
.logo-ring {
    position: absolute; inset: 0; border-radius: 50%;
    background: conic-gradient(from 0deg, #3b82f6, #7c3aed, #10b981, #60a5fa, #3b82f6);
    animation: spinRing 3.5s linear infinite;
}
@keyframes spinRing { to { transform: rotate(360deg); } }
.logo-inner {
    position: absolute; inset: 3px; border-radius: 50%;
    background: #0a0f1e;
    display: flex; align-items: center; justify-content: center;
    font-size: 38px; line-height: 1;
}
.logo-glow {
    position: absolute; inset: -8px; border-radius: 50%;
    background: conic-gradient(from 0deg, rgba(59,130,246,.15), rgba(124,58,237,.15), rgba(16,185,129,.1), rgba(59,130,246,.15));
    animation: spinRing 3.5s linear infinite reverse;
    filter: blur(8px);
}

.hero-title {
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    font-weight: 900; letter-spacing: -2.5px; line-height: 1.05;
    background: linear-gradient(130deg, #60a5fa 0%, #a78bfa 55%, #34d399 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 14px;
    animation: titleShimmer 5s ease-in-out infinite alternate;
}
@keyframes titleShimmer {
    0%   { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}
.hero-sub {
    font-size: 14.5px; color: #475569; max-width: 480px;
    margin: 0 auto 22px; line-height: 1.65;
}
.sys-pills { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
.sys-pill {
    padding: 5px 16px; border-radius: 99px;
    font-size: 12px; font-weight: 600; letter-spacing: 0.2px;
    transition: transform .2s, box-shadow .2s;
}
.sys-pill:hover { transform: translateY(-2px); }
.pill-blue   { background: rgba(59,130,246,.1);  color: #60a5fa; border: 1px solid rgba(59,130,246,.25); }
.pill-teal   { background: rgba(16,185,129,.1);  color: #34d399; border: 1px solid rgba(16,185,129,.25); }
.pill-purple { background: rgba(139,92,246,.1);  color: #a78bfa; border: 1px solid rgba(139,92,246,.25); }

/* ── Divider ─────────────────────────────────────────────────── */
hr { border-color: #0f172a !important; margin: 1.2rem 0 !important; }

/* ── Section labels ─────────────────────────────────────────── */
.section-label {
    font-size: 10px; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: #334155; margin-bottom: 10px;
}
.section-header {
    display: flex; align-items: center; gap: 12px; margin-bottom: 1.2rem;
}
.section-header-text {
    font-size: 10px; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: #334155; white-space: nowrap;
}
.section-header-line { flex: 1; height: 1px; background: #0f172a; }

/* ── Chip buttons (secondary) ───────────────────────────────── */
button[kind="secondary"] {
    background: rgba(255,255,255,.03) !important;
    border: 1px solid #1a2540 !important;
    border-radius: 99px !important;
    color: #4f6282 !important;
    font-size: 12px !important;
    padding: 5px 14px !important;
    font-weight: 500 !important;
    transition: all 0.18s ease !important;
    white-space: nowrap !important;
}
button[kind="secondary"]:hover {
    background: rgba(96,165,250,.08) !important;
    border-color: rgba(96,165,250,.35) !important;
    color: #93c5fd !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(96,165,250,.08) !important;
}

/* ── Primary button ─────────────────────────────────────────── */
button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    font-size: 14px !important;
    box-shadow: 0 4px 20px rgba(99,102,241,.25) !important;
    transition: all 0.2s !important;
}
button[kind="primary"]:hover {
    opacity: .9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 28px rgba(99,102,241,.35) !important;
}

/* ── Text input ─────────────────────────────────────────────── */
div[data-testid="stTextInput"] > div > div > input {
    background: #0c1220 !important;
    border: 1px solid #1a2540 !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
    transition: border-color .2s, box-shadow .2s !important;
}
div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.1) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] label {
    color: #64748b !important; font-size: 12px !important;
    letter-spacing: .5px !important; text-transform: uppercase !important;
    font-weight: 600 !important;
}

/* ── Answer cards ───────────────────────────────────────────── */
.card { border-radius: 14px; overflow: hidden; margin-top: 6px; }

.card-header {
    display: flex; align-items: center; gap: 10px;
    padding: 13px 18px 11px;
    border-bottom: 1px solid rgba(255,255,255,.05);
}
.card-icon { font-size: 17px; line-height: 1; }
.card-title { font-size: 13px; font-weight: 700; line-height: 1.2; }
.card-subtitle { font-size: 10.5px; opacity: .5; margin-top: 2px; }
.card-body { padding: 16px 18px; }
.card-answer { font-size: 14px; line-height: 1.8; }
.card-meta {
    display: flex; align-items: center; gap: 8px;
    margin-top: 14px; padding-top: 12px;
    border-top: 1px solid rgba(255,255,255,.05);
}
.time-chip { display: none; }

/* Blue */
.card-blue { background: linear-gradient(160deg,#091b38,#0c2045); border: 1px solid rgba(59,130,246,.2); }
.card-blue .card-header { background: rgba(59,130,246,.07); }
.card-blue .card-title  { color: #60a5fa; }
.card-blue .card-answer { color: #93c5fd; }
.card-blue .time-chip   { background: rgba(59,130,246,.1); color: #60a5fa; border: 1px solid rgba(59,130,246,.2); }

/* Teal */
.card-teal { background: linear-gradient(160deg,#041a0f,#052516); border: 1px solid rgba(16,185,129,.2); }
.card-teal .card-header { background: rgba(16,185,129,.07); }
.card-teal .card-title  { color: #34d399; }
.card-teal .card-answer { color: #6ee7b7; }
.card-teal .time-chip   { background: rgba(16,185,129,.1); color: #34d399; border: 1px solid rgba(16,185,129,.2); }
.rag-ctx {
    background: rgba(16,185,129,.04); border: 1px solid rgba(16,185,129,.15);
    border-radius: 8px; padding: 10px 14px; margin-top: 14px;
    font-size: 12px; color: #86efac; line-height: 1.65;
}
.rag-ctx-label {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: #34d399; margin-bottom: 7px;
}

/* Purple */
.card-purple { background: linear-gradient(160deg,#100825,#16092e); border: 1px solid rgba(139,92,246,.2); }
.card-purple .card-header { background: rgba(139,92,246,.07); }
.card-purple .card-title  { color: #a78bfa; }
.card-purple .card-answer { color: #c4b5fd; }
.card-purple .time-chip   { background: rgba(139,92,246,.1); color: #a78bfa; border: 1px solid rgba(139,92,246,.2); }

/* ── Question banner ─────────────────────────────────────────── */
.q-banner {
    background: rgba(255,255,255,.02); border: 1px solid #1a2540;
    border-left: 3px solid #6366f1; border-radius: 0 10px 10px 0;
    padding: 10px 16px; margin-bottom: 18px;
    font-size: 13px; color: #64748b; line-height: 1.5;
}
.q-banner strong { color: #e2e8f0; font-weight: 600; }

/* ── Rating section ──────────────────────────────────────────── */
.rate-header { font-size: 13px; font-weight: 700; margin-bottom: 2px; }
.rate-blue   { color: #60a5fa; }
.rate-teal   { color: #34d399; }
.rate-purple { color: #a78bfa; }

/* ── Eval table ──────────────────────────────────────────────── */
.eval-wrap {
    background: #0b1020; border: 1px solid #1a2540;
    border-radius: 14px; overflow: hidden; margin-top: 10px;
}
.eval-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.eval-table th {
    padding: 13px 18px; text-align: center;
    font-weight: 700; font-size: 12px;
    border-bottom: 1px solid #1a2540;
    background: #090e1c; letter-spacing: .3px;
}
.eval-table th:first-child { text-align: left; color: #475569; }
.eval-table th.col-blue   { color: #60a5fa; }
.eval-table th.col-teal   { color: #34d399; }
.eval-table th.col-purple { color: #a78bfa; }
.eval-table td {
    padding: 12px 18px; text-align: center;
    border-bottom: 1px solid #0d1424; color: #cbd5e1;
}
.eval-table td:first-child { text-align: left; color: #475569; font-weight: 600; }
.eval-table tr:last-child td { border-bottom: none; }
.eval-table tr:hover td { background: rgba(255,255,255,.015); }
.badge {
    display: inline-block; padding: 3px 10px;
    border-radius: 99px; font-weight: 700; font-size: 12px;
}
.badge-green  { background: rgba(16,185,129,.1);  color: #34d399; border: 1px solid rgba(16,185,129,.25); }
.badge-yellow { background: rgba(245,158,11,.1);  color: #fbbf24; border: 1px solid rgba(245,158,11,.25); }
.badge-red    { background: rgba(239,68,68,.1);   color: #f87171; border: 1px solid rgba(239,68,68,.25); }
.badge-grey   { background: rgba(100,116,139,.1); color: #64748b; border: 1px solid rgba(100,116,139,.25); }
.metric-note  { color: #334155; font-size: 11px; font-weight: 400; }

/* ── Metric chips ────────────────────────────────────────────── */
.chip { font-size:11px; font-weight:600; padding:3px 9px; border-radius:99px; white-space:nowrap; }
.chip-time   { background:rgba(96,165,250,.08);  color:#60a5fa; border:1px solid rgba(96,165,250,.2); }
.chip-acc    { background:rgba(52,211,153,.08);  color:#34d399; border:1px solid rgba(52,211,153,.2); }
.chip-ground { background:rgba(251,191,36,.08);  color:#fbbf24; border:1px solid rgba(251,191,36,.2); }
.chip-ctx    { background:rgba(244,114,182,.08); color:#f472b6; border:1px solid rgba(244,114,182,.2); }
.chip-rouge  { background:rgba(167,139,250,.08); color:#a78bfa; border:1px solid rgba(167,139,250,.2); }
.card-meta { flex-wrap: wrap; gap: 6px !important; }

/* ── Tabs ────────────────────────────────────────────────────── */
div[data-testid="stTabs"] button[data-baseweb="tab"] {
    font-weight: 600; font-size: 13px; color: #475569;
}
div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
    color: #e2e8f0;
}

/* ── Winner & hallucination badges ──────────────────────────── */
.winner-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(251,191,36,.12); color: #fbbf24;
    border: 1px solid rgba(251,191,36,.3); border-radius: 99px;
    font-size: 11px; font-weight: 700; padding: 3px 10px;
    letter-spacing: .3px;
}
.halluc-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(239,68,68,.1); color: #f87171;
    border: 1px solid rgba(239,68,68,.25); border-radius: 99px;
    font-size: 11px; font-weight: 700; padding: 3px 10px;
}
.card-header-row {
    display: flex; align-items: center;
    justify-content: space-between; width: 100%;
}

/* ── KPI stat cards ──────────────────────────────────────────── */
.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 18px 0; }
.kpi-card {
    border-radius: 14px; padding: 18px 20px;
    display: flex; flex-direction: column; gap: 6px;
}
.kpi-card-blue   { background: linear-gradient(135deg,#091b38,#0c2045); border: 1px solid rgba(59,130,246,.25); }
.kpi-card-teal   { background: linear-gradient(135deg,#041a0f,#052516); border: 1px solid rgba(16,185,129,.25); }
.kpi-card-purple { background: linear-gradient(135deg,#100825,#16092e); border: 1px solid rgba(139,92,246,.25); }
.kpi-system { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; opacity: .6; }
.kpi-system-blue   { color: #60a5fa; }
.kpi-system-teal   { color: #34d399; }
.kpi-system-purple { color: #a78bfa; }
.kpi-stats { display: flex; gap: 18px; flex-wrap: wrap; margin-top: 4px; }
.kpi-stat { display: flex; flex-direction: column; }
.kpi-val { font-size: 26px; font-weight: 900; line-height: 1.1; letter-spacing: -1px; }
.kpi-val-blue   { color: #60a5fa; }
.kpi-val-teal   { color: #34d399; }
.kpi-val-purple { color: #a78bfa; }
.kpi-label { font-size: 10px; color: #475569; font-weight: 600; letter-spacing: .5px; margin-top: 2px; }

/* ── Scrollbar ───────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #080d1a; }
::-webkit-scrollbar-thumb { background: #1a2540; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2d3f5e; }

</style>""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Research Project &nbsp;·&nbsp; NLP &nbsp;·&nbsp; LLM Comparison</div>
    <div class="logo-wrap">
        <div class="logo-glow"></div>
        <div class="logo-ring"></div>
        <div class="logo-inner">🧙</div>
    </div>
    <div class="hero-title">CodeSage</div>
    <div class="hero-sub">
        Comparative study of RAG vs Fine-Tuning for domain-specific QA.<br>
        Ask once &mdash; get answers from all three systems simultaneously.
    </div>
    <div class="sys-pills">
        <span class="sys-pill pill-blue">⚡ Baseline LLM</span>
        <span class="sys-pill pill-teal">🔍 RAG Chatbot</span>
        <span class="sys-pill pill-purple">🧠 Fine-Tuned Model</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Load vector store once ────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Building knowledge base...")
def get_vectorstore():
    if not os.path.exists("data/faiss_index"):
        return build_vectorstore()
    return load_vectorstore()

vs = get_vectorstore()

# ── Reference answers + auto-metrics ─────────────────────────────────────────
@st.cache_data
def load_reference_answers():
    path = "data/reference_answers.json"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}

ref_answers = load_reference_answers()

def safe_answer(text: str) -> str:
    """Escape HTML and convert newlines to <br> so blank lines don't break the markdown HTML block."""
    return html_lib.escape(text).replace('\n', '<br>')

def _cosine(a, b):
    n = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / (n + 1e-8))

def compute_auto_metrics(answer: str, question: str, context: str = "") -> dict:
    if not answer:
        return {}
    try:
        a_emb = np.array(vs.embeddings.embed_query(answer))
        q_emb = np.array(vs.embeddings.embed_query(question))

        # accuracy vs reference answer
        ref = ref_answers.get(question.strip().lower())
        accuracy = None
        rouge_l  = None
        if ref:
            from rouge_score import rouge_scorer as rs
            scorer  = rs.RougeScorer(["rougeL"], use_stemmer=True)
            rouge_l = round(scorer.score(ref, answer)["rougeL"].fmeasure, 3)
            r_emb   = np.array(vs.embeddings.embed_query(ref))
            accuracy = round(max(0.0, _cosine(a_emb, r_emb)), 3)

        # groundedness — how much answer resembles retrieved context
        groundedness = None
        if context and context.strip():
            c_emb = np.array(vs.embeddings.embed_query(context[:1000]))
            groundedness = round(max(0.0, _cosine(a_emb, c_emb)), 3)

        # context relevance — how relevant retrieved context is to question
        ctx_relevance = None
        if context and context.strip():
            c_emb2 = np.array(vs.embeddings.embed_query(context[:1000]))
            ctx_relevance = round(max(0.0, _cosine(q_emb, c_emb2)), 3)

        result = {}
        if accuracy    is not None: result["accuracy"]     = accuracy
        if rouge_l     is not None: result["rouge_l"]      = rouge_l
        if groundedness   is not None: result["groundedness"]  = groundedness
        if ctx_relevance  is not None: result["ctx_relevance"] = ctx_relevance
        return result
    except Exception:
        return {}

def metric_chips(m: dict, time_s: float = None) -> str:
    if not m and time_s is None:
        return ""
    parts = []
    if time_s is not None:
        parts.append(f'<span class="chip chip-time">⏱ {time_s}s</span>')
    if m.get("accuracy") is not None:
        pct = round(m["accuracy"] * 100, 1)
        parts.append(f'<span class="chip chip-acc">🎯 Accuracy {pct}%</span>')
    if m.get("groundedness") is not None:
        parts.append(f'<span class="chip chip-ground">⚓ Grounded {m["groundedness"]:.2f}</span>')
    if m.get("ctx_relevance") is not None:
        parts.append(f'<span class="chip chip-ctx">📄 Ctx.Rel {m["ctx_relevance"]:.2f}</span>')
    if m.get("rouge_l") is not None:
        parts.append(f'<span class="chip chip-rouge">ROUGE-L {m["rouge_l"]:.3f}</span>')
    return "".join(parts)

# ── Benchmark runner ──────────────────────────────────────────────────────────
BENCHMARK_QUESTIONS = [
    "What is binary search?",
    "Stack vs Queue?",
    "Explain merge sort.",
    "What are React hooks?",
    "What is a REST API?",
    "What is dynamic programming?",
]

def run_benchmark(progress_bar=None):
    results = []
    has_ft = os.path.exists("./finetuned_model")
    if has_ft:
        from system3_inference import ask_finetuned
    total = len(BENCHMARK_QUESTIONS)
    for i, q in enumerate(BENCHMARK_QUESTIONS):
        if progress_bar:
            progress_bar.progress((i + 0.5) / total, text=f"({i+1}/{total}) {q[:50]}...")
        r1 = ask_baseline(q)
        r2 = ask_rag(q, vs)
        r3 = ask_finetuned(q) if has_ft else {"answer": "", "response_time": 0}
        m1 = compute_auto_metrics(r1["answer"], q)
        m2 = compute_auto_metrics(r2["answer"], q)
        m3 = compute_auto_metrics(r3["answer"], q)
        results.append({
            "question": q,
            "r1_time": r1["response_time"], "r2_time": r2["response_time"], "r3_time": r3["response_time"],
            "r1_rouge": m1.get("rouge_l", 0), "r2_rouge": m2.get("rouge_l", 0), "r3_rouge": m3.get("rouge_l", 0),
            "r1_sim":   m1.get("accuracy", 0), "r2_sim":   m2.get("accuracy", 0), "r3_sim":   m3.get("accuracy", 0),
        })
    return results

def benchmark_kpis(results):
    n = len(results)
    if n == 0:
        return {}
    def mean(key): return round(sum(r[key] for r in results) / n, 3)
    return {
        "r1_acc":   round(mean("r1_sim") * 100, 1),
        "r2_acc":   round(mean("r2_sim") * 100, 1),
        "r3_acc":   round(mean("r3_sim") * 100, 1),
        "r1_rouge": mean("r1_rouge"),
        "r2_rouge": mean("r2_rouge"),
        "r3_rouge": mean("r3_rouge"),
        "r1_time":  mean("r1_time"),
        "r2_time":  mean("r2_time"),
        "r3_time":  mean("r3_time"),
        "n": n,
    }

# ── 3D Particle background ────────────────────────────────────────────────────
components.html("""
<script>
(function() {
    const doc = window.parent.document;
    if (doc.getElementById('cs-canvas')) return;   // already injected

    const canvas = doc.createElement('canvas');
    canvas.id = 'cs-canvas';
    Object.assign(canvas.style, {
        position: 'fixed', top: '0', left: '0',
        width: '100%', height: '100%',
        pointerEvents: 'none', zIndex: '0',
    });
    doc.body.prepend(canvas);

    const ctx = canvas.getContext('2d');
    const COLORS = ['96,165,250', '167,139,250', '52,211,153'];
    let W, H, pts = [];

    function resize() {
        W = canvas.width  = doc.documentElement.clientWidth;
        H = canvas.height = doc.documentElement.clientHeight;
    }

    function Pt() {
        return {
            x:  Math.random() * W,
            y:  Math.random() * H,
            z:  Math.random() * 800 + 200,        // depth 200–1000
            vx: (Math.random() - .5) * .4,
            vy: (Math.random() - .5) * .4,
            vz: (Math.random() - .5) * .8,
            c:  COLORS[Math.floor(Math.random() * COLORS.length)],
        };
    }

    function project(p) {
        const fov = 600;
        const scale = fov / (fov + p.z);
        return { sx: p.x * scale + W * (1 - scale) / 2,
                 sy: p.y * scale + H * (1 - scale) / 2,
                 scale };
    }

    function init() {
        resize();
        pts = Array.from({ length: 90 }, Pt);
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);

        // Draw connections
        for (let i = 0; i < pts.length; i++) {
            const a = project(pts[i]);
            for (let j = i + 1; j < pts.length; j++) {
                const b = project(pts[j]);
                const dx = a.sx - b.sx, dy = a.sy - b.sy;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 140) {
                    const alpha = (1 - dist / 140) * 0.12 * a.scale;
                    ctx.strokeStyle = `rgba(99,102,241,${alpha})`;
                    ctx.lineWidth = 0.6 * a.scale;
                    ctx.beginPath();
                    ctx.moveTo(a.sx, a.sy);
                    ctx.lineTo(b.sx, b.sy);
                    ctx.stroke();
                }
            }
        }

        // Draw points
        pts.forEach(p => {
            const { sx, sy, scale } = project(p);
            const r = Math.max(0.6, 2.2 * scale);
            const grd = ctx.createRadialGradient(sx, sy, 0, sx, sy, r * 3);
            grd.addColorStop(0,   `rgba(${p.c},${.85 * scale})`);
            grd.addColorStop(0.4, `rgba(${p.c},${.35 * scale})`);
            grd.addColorStop(1,   `rgba(${p.c},0)`);
            ctx.beginPath();
            ctx.arc(sx, sy, r * 3, 0, Math.PI * 2);
            ctx.fillStyle = grd;
            ctx.fill();
        });

        // Move points
        pts.forEach(p => {
            p.x += p.vx; p.y += p.vy; p.z += p.vz;
            if (p.x < 0 || p.x > W)     p.vx *= -1;
            if (p.y < 0 || p.y > H)     p.vy *= -1;
            if (p.z < 200 || p.z > 1000) p.vz *= -1;
        });

        requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize);
    init();
    draw();
})();
</script>
""", height=0)

# ── Input ─────────────────────────────────────────────────────────────────────
st.divider()

sample_questions = [
    "What is binary search?",
    "Stack vs Queue?",
    "Explain merge sort.",
    "What are React hooks?",
    "What is a REST API?",
    "What is dynamic programming?",
]

st.markdown('<div class="section-label">Quick questions</div>', unsafe_allow_html=True)
cols = st.columns(len(sample_questions))
for i, sq in enumerate(sample_questions):
    if cols[i].button(sq, key=f"sq_{i}", use_container_width=True):
        st.session_state.input_question = sq
        st.session_state.auto_run = True
        st.rerun()

st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)

question = st.text_input(
    "Your question",
    placeholder="e.g. What is binary search? / What are React hooks? / Explain merge sort.",
    key="input_question"
)

st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
run_clicked = st.button("⚡  Ask All 3 Systems", type="primary")

# ── Run systems ───────────────────────────────────────────────────────────────
if (run_clicked or st.session_state.auto_run) and question:
    st.session_state.auto_run = False

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.spinner("Baseline LLM generating..."):
            r1 = ask_baseline(question)
    with col2:
        with st.spinner("RAG retrieving + generating..."):
            r2 = ask_rag(question, vs)
    with col3:
        if os.path.exists("./finetuned_model"):
            with st.spinner("Fine-tuned model generating..."):
                from system3_inference import ask_finetuned
                r3 = ask_finetuned(question)
        else:
            r3 = {"answer": "Model not available.", "response_time": 0}

    st.session_state.last_results = {
        "question": question,
        "r1": r1, "r2": r2, "r3": r3,
    }
    st.session_state.auto_metrics = {
        "r1": compute_auto_metrics(r1["answer"], question),
        "r2": compute_auto_metrics(r2["answer"], question, context=r2.get("context_used", "")),
        "r3": compute_auto_metrics(r3["answer"], question),
    }
    _accs = {k: st.session_state.auto_metrics[k].get("accuracy", 0) for k in ("r1","r2","r3")}
    st.session_state.winner = max(_accs, key=_accs.get) if any(_accs.values()) else None
    st.session_state.halluc_flags = {k: (0 < v < 0.4) for k, v in _accs.items()}

# ── Render answers ────────────────────────────────────────────────────────────
if st.session_state.last_results:
    res = st.session_state.last_results
    r1, r2, r3 = res["r1"], res["r2"], res["r3"]

    st.divider()
    st.markdown(f"""
    <div class="q-banner">
        Showing answers for: <strong>"{res['question']}"</strong>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    m   = st.session_state.auto_metrics
    _w  = st.session_state.winner
    _hf = st.session_state.halluc_flags

    def _header_badge(key):
        if _w == key:
            return '<span class="winner-badge">🏆 Best Answer</span>'
        if _hf.get(key):
            return '<span class="halluc-badge">⚠️ Low Confidence</span>'
        return "<span></span>"

    with col1:
        st.markdown(f"""
        <div class="card card-blue">
            <div class="card-header">
                <div class="card-header-row">
                    <div style="display:flex;align-items:center;gap:10px">
                        <span class="card-icon">⚡</span>
                        <div>
                            <div class="card-title">System 1 — Baseline LLM</div>
                            <div class="card-subtitle">Prompt only · No extra knowledge</div>
                        </div>
                    </div>
                    {_header_badge('r1')}
                </div>
            </div>
            <div class="card-body">
                <div class="card-answer">{safe_answer(r1['answer'])}</div>
                <div class="card-meta">
                    {metric_chips(m.get('r1', {}), time_s=r1['response_time'])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card card-teal">
            <div class="card-header">
                <div class="card-header-row">
                    <div style="display:flex;align-items:center;gap:10px">
                        <span class="card-icon">🔍</span>
                        <div>
                            <div class="card-title">System 2 — RAG Chatbot</div>
                            <div class="card-subtitle">Retrieves from knowledge base · Then generates</div>
                        </div>
                    </div>
                    {_header_badge('r2')}
                </div>
            </div>
            <div class="card-body">
                <div class="card-answer">{safe_answer(r2['answer'])}</div>
                <div class="rag-ctx">
                    <div class="rag-ctx-label">📄 Retrieved context</div>
                    {html_lib.escape(r2['context_used'])}
                </div>
                <div class="card-meta">
                    {metric_chips(m.get('r2', {}), time_s=r2['response_time'])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if r3["answer"] == "Model not available.":
            st.markdown("""
            <div class="card card-purple">
                <div class="card-header">
                    <div class="card-header-row">
                        <div style="display:flex;align-items:center;gap:10px">
                            <span class="card-icon">🧠</span>
                            <div>
                                <div class="card-title">System 3 — Fine-Tuned Model</div>
                                <div class="card-subtitle">Qwen2.5-1.5B · LoRA fine-tuning</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-answer" style="opacity:.5">Model not loaded yet.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.warning(
                "Run `system3_finetune_colab.ipynb` on Google Colab, "
                "download `finetuned_model.zip`, and unzip it here."
            )
        else:
            st.markdown(f"""
            <div class="card card-purple">
                <div class="card-header">
                    <div class="card-header-row">
                        <div style="display:flex;align-items:center;gap:10px">
                            <span class="card-icon">🧠</span>
                            <div>
                                <div class="card-title">System 3 — Fine-Tuned Model</div>
                                <div class="card-subtitle">Qwen2.5-1.5B · LoRA on programming Q&A</div>
                            </div>
                        </div>
                        {_header_badge('r3')}
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-answer">{safe_answer(r3['answer'])}</div>
                    <div class="card-meta">
                        {metric_chips(m.get('r3', {}), time_s=r3['response_time'])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Analytics tab ─────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div class="section-header">
    <span class="section-header-text">📊 Analytics &amp; Evaluation</span>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

# ── Benchmark button + KPI cards ──────────────────────────────────────────────
_bm_col, _ = st.columns([2, 5])
with _bm_col:
    if st.button("🔬 Run Auto-Benchmark", key="run_bm", help="Runs all 6 questions through all 3 systems and computes metrics automatically"):
        _prog = st.progress(0, text="Starting benchmark...")
        st.session_state.benchmark_results = run_benchmark(progress_bar=_prog)
        _prog.progress(1.0, text="Done!")
        st.rerun()

_dash = '<span class="badge badge-grey">—</span>'
_bm   = st.session_state.benchmark_results

def badge(val, cls):
    return f'<span class="badge {cls}">{val}</span>'

if _bm:
    _kpi = benchmark_kpis(_bm)
    _systems = ["Baseline LLM", "RAG Chatbot", "Fine-Tuned"]
    _colors  = ["#3b82f6", "#10b981", "#8b5cf6"]
    _layout  = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1e293b", borderwidth=1),
        xaxis=dict(gridcolor="#1a2540", linecolor="#1a2540"),
        yaxis=dict(gridcolor="#1a2540", linecolor="#1a2540"),
        margin=dict(l=20, r=20, t=48, b=20),
    )

    # Win count per system
    _wins = {"r1": 0, "r2": 0, "r3": 0}
    _halluc_counts = {"r1": 0, "r2": 0, "r3": 0}
    for _row in _bm:
        _row_accs = {k: _row[f"{k}_sim"] for k in ("r1","r2","r3")}
        _best = max(_row_accs, key=_row_accs.get)
        if _row_accs[_best] > 0:
            _wins[_best] += 1
        for k in ("r1","r2","r3"):
            if 0 < _row_accs[k] < 0.4:
                _halluc_counts[k] += 1

    _n_q = len(_bm)

    # KPI cards
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card kpi-card-blue">
        <div class="kpi-system kpi-system-blue">⚡ Baseline LLM</div>
        <div class="kpi-stats">
          <div class="kpi-stat"><span class="kpi-val kpi-val-blue">{_kpi['r1_acc']}%</span><span class="kpi-label">Accuracy</span></div>
          <div class="kpi-stat"><span class="kpi-val kpi-val-blue">{_kpi['r1_rouge']}</span><span class="kpi-label">ROUGE-L</span></div>
          <div class="kpi-stat"><span class="kpi-val kpi-val-blue">{_kpi['r1_time']}s</span><span class="kpi-label">Avg Latency</span></div>
          <div class="kpi-stat"><span class="kpi-val kpi-val-blue">{_wins['r1']}/{_n_q}</span><span class="kpi-label">Wins</span></div>
        </div>
      </div>
      <div class="kpi-card kpi-card-teal">
        <div class="kpi-system kpi-system-teal">🔍 RAG Chatbot</div>
        <div class="kpi-stats">
          <div class="kpi-stat"><span class="kpi-val kpi-val-teal">{_kpi['r2_acc']}%</span><span class="kpi-label">Accuracy</span></div>
          <div class="kpi-stat"><span class="kpi-val kpi-val-teal">{_kpi['r2_rouge']}</span><span class="kpi-label">ROUGE-L</span></div>
          <div class="kpi-stat"><span class="kpi-val kpi-val-teal">{_kpi['r2_time']}s</span><span class="kpi-label">Avg Latency</span></div>
          <div class="kpi-stat"><span class="kpi-val kpi-val-teal">{_wins['r2']}/{_n_q}</span><span class="kpi-label">Wins</span></div>
        </div>
      </div>
      <div class="kpi-card kpi-card-purple">
        <div class="kpi-system kpi-system-purple">🧠 Fine-Tuned</div>
        <div class="kpi-stats">
          <div class="kpi-stat"><span class="kpi-val kpi-val-purple">{_kpi['r3_acc']}%</span><span class="kpi-label">Accuracy</span></div>
          <div class="kpi-stat"><span class="kpi-val kpi-val-purple">{_kpi['r3_rouge']}</span><span class="kpi-label">ROUGE-L</span></div>
          <div class="kpi-stat"><span class="kpi-val kpi-val-purple">{_kpi['r3_time']}s</span><span class="kpi-label">Avg Latency</span></div>
          <div class="kpi-stat"><span class="kpi-val kpi-val-purple">{_wins['r3']}/{_n_q}</span><span class="kpi-label">Wins</span></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Benchmark across {_n_q} questions · semantic similarity via embeddings · ROUGE-L vs reference answers")

    # Charts
    ch1, ch2 = st.columns(2)
    with ch1:
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(name="Accuracy %", x=_systems,
            y=[_kpi['r1_acc'], _kpi['r2_acc'], _kpi['r3_acc']],
            marker_color=_colors, text=[f"{v}%" for v in [_kpi['r1_acc'],_kpi['r2_acc'],_kpi['r3_acc']]], textposition="auto"))
        fig1.add_trace(go.Bar(name="ROUGE-L ×100", x=_systems,
            y=[round(_kpi['r1_rouge']*100,1), round(_kpi['r2_rouge']*100,1), round(_kpi['r3_rouge']*100,1)],
            marker_color=_colors, opacity=0.55,
            text=[f"{round(v*100,1)}" for v in [_kpi['r1_rouge'],_kpi['r2_rouge'],_kpi['r3_rouge']]], textposition="auto"))
        fig1.update_layout(**_layout, barmode="group", height=300,
            title=dict(text="Accuracy % vs ROUGE-L (scaled ×100)", font=dict(color="#e2e8f0", size=14)))
        st.plotly_chart(fig1, use_container_width=True)

    with ch2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Avg Latency (s)", x=_systems,
            y=[_kpi['r1_time'], _kpi['r2_time'], _kpi['r3_time']],
            marker_color=_colors, text=[f"{v}s" for v in [_kpi['r1_time'],_kpi['r2_time'],_kpi['r3_time']]], textposition="auto"))
        fig2.add_trace(go.Bar(name="Low Confidence answers", x=_systems,
            y=[_halluc_counts['r1'], _halluc_counts['r2'], _halluc_counts['r3']],
            marker_color=_colors, opacity=0.55,
            text=[str(v) for v in [_halluc_counts['r1'],_halluc_counts['r2'],_halluc_counts['r3']]], textposition="auto"))
        fig2.update_layout(**_layout, barmode="group", height=300,
            title=dict(text="Avg Latency (s) · Low-Confidence Answers", font=dict(color="#e2e8f0", size=14)))
        st.plotly_chart(fig2, use_container_width=True)

    def _col_acc(v): return "badge-green" if v >= 75 else ("badge-yellow" if v >= 55 else "badge-red")
    def _col_rou(v): return "badge-green" if v >= 0.4 else ("badge-yellow" if v >= 0.2 else "badge-red")
    def _col_time(v): return "badge-green" if v <= 1.0 else ("badge-yellow" if v <= 2.5 else "badge-red")
    def _col_halluc(v, n): return "badge-green" if v == 0 else ("badge-yellow" if v <= n//2 else "badge-red")

    bm_row_acc    = tuple(badge(f"{_kpi[f'r{i}_acc']}%",   _col_acc(_kpi[f'r{i}_acc']))   for i in (1,2,3))
    bm_row_rouge  = tuple(badge(f"{_kpi[f'r{i}_rouge']}",  _col_rou(_kpi[f'r{i}_rouge'])) for i in (1,2,3))
    bm_row_time   = tuple(badge(f"{_kpi[f'r{i}_time']}s",  _col_time(_kpi[f'r{i}_time'])) for i in (1,2,3))
    bm_row_wins   = tuple(badge(f"{_wins[f'r{i}']}/{_n_q}", "badge-green" if _wins[f'r{i}']==max(_wins.values()) else "badge-yellow") for i in (1,2,3))
    bm_row_halluc = tuple(badge(f"{_halluc_counts[f'r{i}']}",_col_halluc(_halluc_counts[f'r{i}'],_n_q)) for i in (1,2,3))
else:
    st.caption("Run the benchmark to populate the analytics table.")
    bm_row_acc = bm_row_rouge = bm_row_time = bm_row_wins = bm_row_halluc = (_dash, _dash, _dash)

st.markdown(f"""
<div class="eval-wrap">
<table class="eval-table">
  <thead>
    <tr>
      <th>Metric</th>
      <th class="col-blue">⚡ System 1<br><span style="font-weight:500;font-size:11px;opacity:.6">Baseline LLM</span></th>
      <th class="col-teal">🔍 System 2<br><span style="font-weight:500;font-size:11px;opacity:.6">RAG Chatbot</span></th>
      <th class="col-purple">🧠 System 3<br><span style="font-weight:500;font-size:11px;opacity:.6">Fine-Tuned</span></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Answer Accuracy <span class="metric-note">(%, semantic similarity vs reference)</span></td>
      <td>{bm_row_acc[0]}</td><td>{bm_row_acc[1]}</td><td>{bm_row_acc[2]}</td>
    </tr>
    <tr>
      <td>ROUGE-L Score <span class="metric-note">(lexical overlap vs reference)</span></td>
      <td>{bm_row_rouge[0]}</td><td>{bm_row_rouge[1]}</td><td>{bm_row_rouge[2]}</td>
    </tr>
    <tr>
      <td>Low-Confidence Answers <span class="metric-note">(accuracy &lt; 40%, possible hallucination)</span></td>
      <td>{bm_row_halluc[0]}</td><td>{bm_row_halluc[1]}</td><td>{bm_row_halluc[2]}</td>
    </tr>
    <tr>
      <td>Avg Response Time <span class="metric-note">(seconds, auto)</span></td>
      <td>{bm_row_time[0]}</td><td>{bm_row_time[1]}</td><td>{bm_row_time[2]}</td>
    </tr>
    <tr>
      <td>Questions Won <span class="metric-note">(highest accuracy per question)</span></td>
      <td>{bm_row_wins[0]}</td><td>{bm_row_wins[1]}</td><td>{bm_row_wins[2]}</td>
    </tr>
  </tbody>
</table>
</div>
""", unsafe_allow_html=True)

if _bm:
    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    if st.button("Clear Benchmark"):
        st.session_state.benchmark_results = []
        st.rerun()

# ── About ──────────────────────────────────────────────────────────────────────
st.divider()
with st.expander("About CodeSage"):
    st.markdown("""
**Project:** CodeSage — Comparative Study of RAG and Fine-Tuning for Domain-Specific QA
**Domain:** Programming Tutor (DSA + Web Development)

| System | Description |
|--------|-------------|
| Baseline | Llama 3.1 8B via Groq · system prompt only |
| RAG | FAISS vector store + HuggingFace embeddings + Llama 3.1 8B via Groq |
| Fine-tuned | Qwen2.5-1.5B-Instruct fine-tuned via LoRA on 20 programming Q&A pairs |

Drop any PDF into `data/pdfs/` and delete `data/faiss_index/` to rebuild the RAG knowledge base with it included.
""")
