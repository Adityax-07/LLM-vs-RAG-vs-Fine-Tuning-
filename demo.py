import os
import streamlit as st
import streamlit.components.v1 as components
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
.time-chip {
    font-size: 11px; font-weight: 600;
    padding: 3px 10px; border-radius: 99px;
}

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
    st.session_state.rating_submitted = False

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

    with col1:
        st.markdown(f"""
        <div class="card card-blue">
            <div class="card-header">
                <span class="card-icon">⚡</span>
                <div>
                    <div class="card-title">System 1 — Baseline LLM</div>
                    <div class="card-subtitle">Prompt only · No extra knowledge</div>
                </div>
            </div>
            <div class="card-body">
                <div class="card-answer">{r1['answer']}</div>
                <div class="card-meta">
                    <span class="time-chip">⏱ {r1['response_time']}s</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card card-teal">
            <div class="card-header">
                <span class="card-icon">🔍</span>
                <div>
                    <div class="card-title">System 2 — RAG Chatbot</div>
                    <div class="card-subtitle">Retrieves from knowledge base · Then generates</div>
                </div>
            </div>
            <div class="card-body">
                <div class="card-answer">{r2['answer']}</div>
                <div class="rag-ctx">
                    <div class="rag-ctx-label">📄 Retrieved context</div>
                    {r2['context_used']}
                </div>
                <div class="card-meta">
                    <span class="time-chip">⏱ {r2['response_time']}s</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if r3["answer"] == "Model not available.":
            st.markdown("""
            <div class="card card-purple">
                <div class="card-header">
                    <span class="card-icon">🧠</span>
                    <div>
                        <div class="card-title">System 3 — Fine-Tuned Model</div>
                        <div class="card-subtitle">TinyLlama · LoRA fine-tuning</div>
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
                    <span class="card-icon">🧠</span>
                    <div>
                        <div class="card-title">System 3 — Fine-Tuned Model</div>
                        <div class="card-subtitle">TinyLlama 1.1B · LoRA on programming Q&A</div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-answer">{r3['answer']}</div>
                    <div class="card-meta">
                        <span class="time-chip">⏱ {r3['response_time']}s</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Rating section ─────────────────────────────────────────────────────────────
if st.session_state.last_results and not st.session_state.rating_submitted:
    st.divider()
    st.markdown("""
    <div class="section-header">
        <span class="section-header-text">Rate the answers</span>
        <div class="section-header-line"></div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Your ratings populate the live evaluation table below.")

    rc1, rc2, rc3 = st.columns(3)

    with rc1:
        st.markdown('<div class="rate-header rate-blue">System 1 — Baseline LLM</div>', unsafe_allow_html=True)
        c1_correct  = st.slider("Correctness (1–5)",  1, 5, 3, key="c1_correct")
        c1_halluc   = st.checkbox("Hallucination detected?", key="c1_halluc")
        c1_complete = st.slider("Completeness (1–5)", 1, 5, 3, key="c1_complete")

    with rc2:
        st.markdown('<div class="rate-header rate-teal">System 2 — RAG Chatbot</div>', unsafe_allow_html=True)
        c2_correct  = st.slider("Correctness (1–5)",  1, 5, 3, key="c2_correct")
        c2_halluc   = st.checkbox("Hallucination detected?", key="c2_halluc")
        c2_complete = st.slider("Completeness (1–5)", 1, 5, 3, key="c2_complete")

    with rc3:
        st.markdown('<div class="rate-header rate-purple">System 3 — Fine-Tuned</div>', unsafe_allow_html=True)
        c3_correct  = st.slider("Correctness (1–5)",  1, 5, 3, key="c3_correct")
        c3_halluc   = st.checkbox("Hallucination detected?", key="c3_halluc")
        c3_complete = st.slider("Completeness (1–5)", 1, 5, 3, key="c3_complete")

    if st.button("Submit Ratings", type="primary"):
        res = st.session_state.last_results
        st.session_state.ratings.append({
            "question":    res["question"],
            "c1_correct":  c1_correct,  "c2_correct":  c2_correct,  "c3_correct":  c3_correct,
            "c1_halluc":   1 if c1_halluc  else 0,
            "c2_halluc":   1 if c2_halluc  else 0,
            "c3_halluc":   1 if c3_halluc  else 0,
            "c1_complete": c1_complete, "c2_complete": c2_complete, "c3_complete": c3_complete,
            "c1_time":     res["r1"]["response_time"],
            "c2_time":     res["r2"]["response_time"],
            "c3_time":     res["r3"]["response_time"],
        })
        st.session_state.rating_submitted = True
        st.success(f"Rating saved! Total questions rated: {len(st.session_state.ratings)}")
        st.rerun()

# ── Metrics table ──────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div class="section-header">
    <span class="section-header-text">Evaluation metrics</span>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

ratings = st.session_state.ratings
n = len(ratings)

if n == 0:
    st.caption("No ratings yet. Ask a question and rate the answers to populate this table.")
    def badge(val, _n):
        return '<span class="badge badge-grey">—</span>'
else:
    st.caption(f"Based on **{n} question(s)** rated by you. Response time is measured automatically.")

    def avg(key): return round(sum(r[key] for r in ratings) / n, 2)
    def pct(key): return round(sum(r[key] for r in ratings) / n * 100)

    def color_correct(v):
        return "badge-green" if v >= 4.0 else ("badge-yellow" if v >= 3.0 else "badge-red")
    def color_halluc(v):
        return "badge-green" if v <= 15  else ("badge-yellow" if v <= 30  else "badge-red")
    def color_complete(v):
        return "badge-green" if v >= 4.0 else ("badge-yellow" if v >= 3.0 else "badge-red")
    def color_time(v):
        return "badge-green" if v <= 1.0 else ("badge-yellow" if v <= 2.0 else "badge-red")

    def badge(val, cls):
        return f'<span class="badge {cls}">{val}</span>'

    v_c1,v_c2,v_c3 = avg("c1_correct"), avg("c2_correct"), avg("c3_correct")
    v_h1,v_h2,v_h3 = pct("c1_halluc"),  pct("c2_halluc"),  pct("c3_halluc")
    v_p1,v_p2,v_p3 = avg("c1_complete"),avg("c2_complete"),avg("c3_complete")
    v_t1,v_t2,v_t3 = avg("c1_time"),    avg("c2_time"),    avg("c3_time")

    row_correct  = (badge(f"{v_c1}/5", color_correct(v_c1)),  badge(f"{v_c2}/5", color_correct(v_c2)),  badge(f"{v_c3}/5", color_correct(v_c3)))
    row_halluc   = (badge(f"{v_h1}%",  color_halluc(v_h1)),   badge(f"{v_h2}%",  color_halluc(v_h2)),   badge(f"{v_h3}%",  color_halluc(v_h3)))
    row_complete = (badge(f"{v_p1}/5", color_complete(v_p1)), badge(f"{v_p2}/5", color_complete(v_p2)), badge(f"{v_p3}/5", color_complete(v_p3)))
    row_time     = (badge(f"{v_t1}s",  color_time(v_t1)),     badge(f"{v_t2}s",  color_time(v_t2)),     badge(f"{v_t3}s",  color_time(v_t3)))

if n == 0:
    dash = '<span class="badge badge-grey">—</span>'
    row_correct = row_halluc = row_complete = row_time = (dash, dash, dash)

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
</div>
""", unsafe_allow_html=True)

if n > 0:
    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    if st.button("Clear All Ratings"):
        st.session_state.ratings = []
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
| Fine-tuned | TinyLlama 1.1B fine-tuned via LoRA on 20 programming Q&A pairs |
""")
