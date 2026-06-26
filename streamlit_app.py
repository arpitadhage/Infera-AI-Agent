import streamlit as st
import requests

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
API_URL = "http://127.0.0.1:8000/run-agent"

SUPPORTED_TYPES = [
    "pdf", "png", "jpg", "jpeg", "webp", "bmp",
    "mp3", "mp4", "wav", "m4a", "ogg",
    "docx", "txt", "md", "csv",
    "py", "java", "cpp", "js", "ts", "c", "cs", "rb", "go", "php", "html", "rs",
]

INTENT_ICONS = {
    "summarization":         "📝",
    "sentiment_analysis":    "💬",
    "code_explanation":      "💻",
    "comparison":            "⚖️",
    "cross_input_reasoning": "🔗",
    "conversation":          "🗣️",
}

st.set_page_config(
    page_title="DataSmith AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.agent-title {
    font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(135deg, #6C63FF, #3ecfcf);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.agent-sub { color: #888; font-size: 0.9rem; margin-bottom: 1rem; }
.bubble-user {
    background: linear-gradient(135deg,#6C63FF18,#3ecfcf18);
    border-left: 3px solid #6C63FF; border-radius: 0 10px 10px 0;
    padding: 10px 16px; margin: 6px 0; color: #e0e0e0;
}
.bubble-bot {
    background: #1a1d27; border-left: 3px solid #3ecfcf;
    border-radius: 0 10px 10px 0; padding: 10px 16px;
    margin: 6px 0; color: #d0d0d0; white-space: pre-wrap;
}
.lbl { font-size:0.72rem; font-weight:700; letter-spacing:.06em; margin-bottom:4px; }
.lbl-u { color:#6C63FF; } .lbl-b { color:#3ecfcf; }
.pill {
    display:inline-block; background:#1e2130; border:1px solid #3ecfcf44;
    border-radius:20px; padding:2px 10px; margin:2px;
    font-size:0.74rem; color:#3ecfcf;
}
.intent-badge {
    display:inline-block; background:#6C63FF22; border:1px solid #6C63FF55;
    border-radius:5px; padding:1px 9px; font-size:0.75rem; color:#9d97ff; margin-bottom:6px;
}
.ftag {
    display:inline-block; background:#1e2130; border:1px solid #fff2;
    border-radius:4px; padding:1px 7px; margin:2px; font-size:0.73rem; color:#aaa;
}
            
div.stButton > button {
    background: linear-gradient(135deg,#2563EB,#3B82F6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    height: 45px !important;
    transition: all .25s ease;
}

div.stButton > button:hover{
    background: linear-gradient(135deg,#1D4ED8,#2563EB) !important;
    transform: translateY(-1px);
    box-shadow:0 0 15px rgba(37,99,235,.45);
}

div.stButton > button:active{
    transform:scale(.98);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for key, default in [("chat", []), ("pending", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "input_key" not in st.session_state:
        st.session_state.input_key = 0

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 DataSmith")
    st.caption("Multi-Modal AI Agent · Groq-powered")
    st.divider()
    st.markdown("**⚙️ Capabilities**")
    for cap in [
        "📄 PDF extraction", "🖼️ Image OCR",
        "🎙️ Audio → Whisper", "🐍 Code explanation",
        "💬 Sentiment analysis", "⚖️ Multi-file comparison",
        "🔗 Cross-input reasoning", "💬 General chat",
    ]:
        st.markdown(f"- {cap}")
    st.divider()
    st.markdown("**💡 Example queries**")
    st.code("Upload PDF + Audio → Compare them")
    st.code("Upload .py file → Explain this code")
    st.code("Upload review.txt → Analyze sentiment")
    st.code("Upload 2 PDFs → Are these the same?")
    st.divider()
    turns = sum(1 for m in st.session_state.chat if m["role"] == "user")
    st.metric("Conversation turns", turns)
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat = []
        st.session_state.pending = None
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="agent-title">🤖 DataSmith AI Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="agent-sub">Multi-modal · PDF · Audio · Images · Code · Comparison · Groq LLM</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CHAT DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
for msg in st.session_state.chat:
    if msg["role"] == "user":
        ftags = "".join(f'<span class="ftag">📎 {f}</span>' for f in msg.get("files", []))
        extra = f"<br>{ftags}" if ftags else ""
        st.markdown(
            f'<div class="bubble-user"><div class="lbl lbl-u">YOU</div>{msg["content"]}{extra}</div>',
            unsafe_allow_html=True,
        )
    else:
        meta = msg.get("meta", {})
        intent = meta.get("intent", "")
        plan = meta.get("plan", [])
        icon = INTENT_ICONS.get(intent, "🤖")
        ibadge = f'<span class="intent-badge">{icon} {intent.replace("_"," ").title()}</span><br>' if intent else ""
        ppills = "".join(f'<span class="pill">→ {s}</span>' for s in plan)
        prow = f'<div style="margin-top:8px;font-size:.72rem;color:#555">{ppills}</div>' if ppills else ""
        st.markdown(
            f'<div class="bubble-bot"><div class="lbl lbl-b">DATASMITH</div>{ibadge}{msg["content"]}{prow}</div>',
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────────────────────
# INPUT
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
query = st.text_area(
    "Your message",
    placeholder="Ask anything : summarize · compare · explain code · analyze sentiment...",
    height=75,
    label_visibility="collapsed",
    key=f"query_input_{st.session_state.input_key}",
)
uploaded = st.file_uploader(
    "📎 Upload files — mix any types (PDF, Audio, Image, Code, Text)",
    type=SUPPORTED_TYPES,
    accept_multiple_files=True,
    key=f"file_uploader_{st.session_state.uploader_key}",
)

col1, col2 = st.columns([5, 1])
with col1:
    if uploaded:
        st.caption(f"📎 {len(uploaded)} file(s) ready: {', '.join(f.name for f in uploaded)}")
with col2:
    send_clicked = st.button(" Send", type="primary", use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# STAGE → SEND → DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
if send_clicked and (query.strip() or uploaded):
    # Stage everything NOW before Streamlit clears uploader
    st.session_state.pending = {
        "query": query.strip(),
        "files": [(f.name, f.getvalue()) for f in uploaded] if uploaded else [],
    }
    # Add user bubble immediately
    st.session_state.chat.append({
        "role": "user",
        "content": query.strip() or "(files only)",
        "files": [f.name for f in uploaded] if uploaded else [],
    })
    st.rerun()

# ── Process pending request ──────────────────────────────────────────────────
if st.session_state.pending:
    pending = st.session_state.pending
    st.session_state.pending = None   # clear immediately

    with st.spinner("🧠 DataSmith is thinking..."):
        try:
            files_payload = [
                ("files", (fname, data))
                for fname, data in pending["files"]
            ]
            response = requests.post(
                API_URL,
                data={"query": pending["query"] or "process the uploaded files"},
                files=files_payload if files_payload else None,
                timeout=120,
            )
            result = response.json()
            bot_reply = result.get("response", "⚠️ No response generated.")
            meta = {"intent": result.get("intent", ""), "plan": result.get("plan", [])}
        except requests.exceptions.ConnectionError:
            bot_reply = (
                "❌ **Cannot connect to the backend.**\n\n"
                "Start it with:\n```bash\ncd datasmith\nuvicorn main:app --reload\n```"
            )
            meta = {}
        except Exception as e:
            bot_reply = f"❌ Error: {e}"
            meta = {}

    st.session_state.chat.append({
    "role": "bot",
    "content": bot_reply,
    "meta": meta
    })

# Clear query textbox
   # st.session_state.query_input = ""
    st.session_state.input_key += 1

# Reset file uploader
    st.session_state.uploader_key += 1
    

    st.rerun()
