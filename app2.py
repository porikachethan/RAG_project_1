"""
HR Policy Assistant - Streamlit frontend, v2 ("Teal & Coral" design).

Sections:
  1. Page config & imports
  2. Constants
  3. Custom CSS (explicit colors, safe fonts)
  4. Session-state helpers
  5. Backend wrapper
  6. UI components
  7. Main app
"""

import streamlit as st

# ----------------------------------------------------------------------------
# 1. PAGE CONFIG (must be the first Streamlit call)
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="HR Policy Assistant",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="expanded",
)

from hr_assistant.pipeline import build_hr_assistant, ask  # noqa: E402

# ----------------------------------------------------------------------------
# 2. CONSTANTS
# ----------------------------------------------------------------------------
TOPICS = [
    ("🏥", "Sick leave", "How many sick leaves do employees get?"),
    ("🌴", "Annual leave", "What is the annual leave policy?"),
    ("📅", "Notice period", "What is the notice period?"),
    ("🏠", "Work from home", "What is the work-from-home policy?"),
]

DISCLAIMER = "Answers are based on the available HR policy documents."
NOT_FOUND_MSG = "I couldn't find this information in the available HR policy documents."
ERROR_MSG = "Sorry, something went wrong while getting your answer. Please try again."

MAX_QUESTION_CHARS = 500          # token saving: cap question length
USE_BREVITY_HINT = False          # set True if SYSTEM_PROMPT is not concise
BREVITY_HINT = " (Answer in 2-4 sentences, using only the HR policy documents.)"

AVATAR_USER = "🙂"
AVATAR_BOT = "🧭"

# ----------------------------------------------------------------------------
# 3. CUSTOM CSS
#    - No external fonts, no global font override (keeps icons working).
#    - Every text color is set explicitly so nothing turns invisible.
# ----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
:root {
    --bg: #faf7f2;
    --card: #ffffff;
    --ink: #1f2937;
    --muted: #6b7280;
    --line: #e8e2d9;
    --teal: #0d9488;
    --teal-dark: #0f766e;
    --coral: #f43f5e;
    --navy: #0f172a;
    --navy-2: #1e293b;
    --font: "Segoe UI", system-ui, -apple-system, Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* Apply font only to text elements, never to icons */
.stMarkdown, .stMarkdown p, .stMarkdown li, .stCaption, .stButton button p,
textarea, input, h1, h2, h3, .brand, .hero, .topbar, .topic-card, .typing-wrap {
    font-family: var(--font);
}

.stApp { background: var(--bg); }

/* Main text colors (explicit) */
div[data-testid="stMain"] .stMarkdown p,
div[data-testid="stMain"] .stMarkdown li,
div[data-testid="stMain"] .stMarkdown span,
.main .stMarkdown p, .main .stMarkdown li {
    color: var(--ink);
    font-size: 1rem;
    line-height: 1.65;
}

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

.block-container { max-width: 800px; padding-top: 1.2rem; padding-bottom: 7rem; }

/* ---------- Sidebar (dark navy) ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--navy) 0%, var(--navy-2) 100%);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] .stCaption p,
section[data-testid="stSidebar"] label {
    color: #cbd5e1 !important;
}
.brand { display: flex; align-items: center; gap: .75rem; padding: .3rem 0 1rem 0; }
.brand-logo {
    width: 46px; height: 46px; border-radius: 14px; display: grid; place-items: center;
    font-size: 1.5rem; background: linear-gradient(135deg, #2dd4bf, #0d9488);
    box-shadow: 0 8px 20px rgba(45,212,191,.28);
}
.brand-title { color: #ffffff; font-weight: 700; font-size: 1.1rem; line-height: 1.2; }
.brand-sub   { color: #94a3b8; font-size: .78rem; }
.side-label {
    color: #2dd4bf; font-size: .68rem; font-weight: 700; letter-spacing: .12em;
    text-transform: uppercase; margin: 1.4rem 0 .6rem 0;
}
.side-item {
    color: #e2e8f0; font-size: .86rem; padding: .55rem .75rem; margin-bottom: .4rem;
    border-radius: 10px; background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.08);
}
.status {
    display: inline-flex; align-items: center; gap: .45rem; color: #86efac;
    font-size: .78rem; background: rgba(34,197,94,.12);
    border: 1px solid rgba(34,197,94,.3); padding: .2rem .65rem; border-radius: 999px;
}
.dot { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; animation: pulse 1.8s infinite; }

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(244,63,94,.12); border: 1px solid rgba(244,63,94,.45);
    border-radius: 10px; transition: all .2s ease;
}
section[data-testid="stSidebar"] .stButton > button p { color: #fecdd3 !important; font-weight: 600; }
section[data-testid="stSidebar"] .stButton > button:hover { background: rgba(244,63,94,.25); }
section[data-testid="stSidebar"] .stButton > button:disabled { opacity: .4; }

/* ---------- Top bar ---------- */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    background: var(--card); border: 1px solid var(--line); border-radius: 16px;
    padding: .8rem 1.1rem; margin-bottom: 1.2rem;
    box-shadow: 0 4px 16px rgba(15,23,42,.04);
}
.topbar-title { color: var(--ink); font-weight: 700; font-size: 1rem; }
.topbar-sub   { color: var(--muted); font-size: .8rem; }
.topbar-tag {
    color: var(--teal-dark); background: #ccfbf1; font-size: .72rem; font-weight: 700;
    padding: .25rem .65rem; border-radius: 999px;
}

/* ---------- Welcome ---------- */
.hero { padding: 1.6rem 0 .6rem 0; animation: rise .6s ease both; }
.hero-hi { color: var(--coral); font-weight: 700; font-size: .85rem; letter-spacing: .08em; text-transform: uppercase; }
.hero h1 { color: var(--ink); font-size: 2.1rem; font-weight: 800; line-height: 1.15; margin: .4rem 0 .6rem 0; }
.hero h1 em { font-style: normal; color: var(--teal); }
.hero p { color: var(--muted); font-size: 1rem; max-width: 520px; margin: 0; }
.suggest-title {
    color: var(--muted); font-size: .72rem; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; margin: 1.6rem 0 .7rem 0;
}

/* Suggestion cards (main-area buttons) */
div[data-testid="stMain"] .stButton > button, .main .stButton > button {
    background: var(--card); border: 1px solid var(--line); border-radius: 14px;
    min-height: 3.4rem; padding: .7rem 1rem; justify-content: flex-start; text-align: left;
    border-left: 4px solid var(--teal); transition: all .2s ease;
    box-shadow: 0 2px 8px rgba(15,23,42,.04);
}
div[data-testid="stMain"] .stButton > button p, .main .stButton > button p {
    color: var(--ink) !important; font-weight: 600; font-size: .92rem; text-align: left;
}
div[data-testid="stMain"] .stButton > button:hover, .main .stButton > button:hover {
    border-color: var(--teal); border-left-color: var(--coral);
    transform: translateY(-2px); box-shadow: 0 10px 24px rgba(13,148,136,.15);
}

/* ---------- Chat messages ---------- */
div[data-testid="stChatMessage"] {
    background: var(--card); border: 1px solid var(--line);
    border-left: 4px solid var(--teal); border-radius: 6px 18px 18px 18px;
    padding: .9rem 1.1rem; margin-bottom: .9rem; width: fit-content; max-width: 92%;
    box-shadow: 0 3px 12px rgba(15,23,42,.05); animation: rise .35s ease both;
}
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] span { color: var(--ink); }

/* User messages: right-aligned teal bubble with white text */
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse; margin-left: auto;
    background: linear-gradient(135deg, var(--teal-dark), var(--teal));
    border: none; border-radius: 18px 18px 6px 18px;
    box-shadow: 0 8px 20px rgba(13,148,136,.28);
}
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) li,
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) span {
    color: #ffffff !important;
}

/* ---------- Typing indicator ---------- */
.typing-wrap { display: flex; align-items: center; gap: .6rem; color: var(--muted); font-size: .9rem; }
.typing { display: inline-flex; gap: 4px; }
.typing span {
    width: 8px; height: 8px; border-radius: 50%; background: var(--teal);
    animation: bounce 1.2s infinite ease-in-out;
}
.typing span:nth-child(2) { animation-delay: .15s; background: #14b8a6; }
.typing span:nth-child(3) { animation-delay: .3s; background: var(--coral); }

/* ---------- Chat input ---------- */
div[data-testid="stBottom"], div[data-testid="stBottom"] > div,
div[data-testid="stBottomBlockContainer"] { background: var(--bg) !important; }
div[data-testid="stChatInput"] {
    background: #ffffff; border: 2px solid var(--line); border-radius: 16px;
    box-shadow: 0 8px 28px rgba(15,23,42,.08);
}
div[data-testid="stChatInput"]:focus-within { border-color: var(--teal); }
div[data-testid="stChatInput"] textarea {
    color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important;
    background: #ffffff !important; font-size: 1rem;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: #9ca3af !important; -webkit-text-fill-color: #9ca3af !important;
}
div[data-testid="stChatInput"] button { background: var(--teal) !important; border-radius: 12px; }
div[data-testid="stChatInput"] button svg { fill: #ffffff !important; color: #ffffff !important; }

.disclaimer { text-align: center; color: var(--muted); font-size: .76rem; margin-top: .8rem; }

@keyframes rise   { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
@keyframes bounce { 0%, 80%, 100% { transform: scale(.6); opacity: .5; } 40% { transform: scale(1); opacity: 1; } }
@keyframes pulse  { 0%, 100% { opacity: 1; } 50% { opacity: .35; } }

/* ---------- Mobile ---------- */
@media (max-width: 640px) {
    .block-container { padding: .8rem .7rem 7rem .7rem; }
    .hero h1 { font-size: 1.6rem; }
    .topbar-tag { display: none; }
    div[data-testid="stChatMessage"] { max-width: 100%; padding: .7rem .8rem; }
}
</style>
"""

TYPING_HTML = """
<div class="typing-wrap">
    <div class="typing"><span></span><span></span><span></span></div>
    Checking the HR policies...
</div>
"""

# ----------------------------------------------------------------------------
# 4. SESSION-STATE HELPERS
# ----------------------------------------------------------------------------
def init_session_state() -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("agent", None)
    st.session_state.setdefault("pending_question", None)


def clear_chat() -> None:
    """Reset the conversation but keep the initialized agent."""
    st.session_state.messages = []
    st.session_state.pending_question = None


def queue_question(question: str) -> None:
    st.session_state.pending_question = question


# ----------------------------------------------------------------------------
# 5. BACKEND WRAPPER
# ----------------------------------------------------------------------------
def get_agent():
    """Build the agent once per session and reuse it."""
    if st.session_state.agent is None:
        st.session_state.agent = build_hr_assistant()
    return st.session_state.agent


def get_answer(question: str) -> str:
    """Send only the current question (no history) to keep token usage low."""
    question = question.strip()[:MAX_QUESTION_CHARS]
    if USE_BREVITY_HINT:
        question += BREVITY_HINT
    try:
        answer = ask(get_agent(), question)
        answer = answer if isinstance(answer, str) else str(answer)
        return answer.strip() or NOT_FOUND_MSG
    except Exception as exc:  # noqa: BLE001
        print(f"[HR Assistant error] {type(exc).__name__}: {exc}")
        return ERROR_MSG


# ----------------------------------------------------------------------------
# 6. UI COMPONENTS
# ----------------------------------------------------------------------------
def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-logo">🧭</div>
                <div>
                    <div class="brand-title">HR Assistant</div>
                    <div class="brand-sub">Your policy guide</div>
                </div>
            </div>
            <span class="status"><span class="dot"></span>Online</span>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="side-label">Topics I can help with</div>', unsafe_allow_html=True)
        for icon, title, _ in TOPICS:
            st.markdown(f'<div class="side-item">{icon}&nbsp; {title}</div>', unsafe_allow_html=True)

        st.markdown('<div class="side-label">Conversation</div>', unsafe_allow_html=True)
        st.button(
            "🗑️  Clear chat",
            on_click=clear_chat,
            use_container_width=True,
            disabled=not st.session_state.messages,
        )
        st.caption(f"{len(st.session_state.messages)} messages in this session")

        st.markdown('<div class="side-label">Note</div>', unsafe_allow_html=True)
        st.caption(DISCLAIMER)


def render_topbar() -> None:
    st.markdown(
        """
        <div class="topbar">
            <div>
                <div class="topbar-title">HR Policy Assistant</div>
                <div class="topbar-sub">Quick, accurate answers from your policy documents</div>
            </div>
            <div class="topbar-tag">AI POWERED</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_welcome() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-hi">Welcome</div>
            <h1>Got an HR question?<br><em>Ask away.</em></h1>
            <p>I can help with leave, notice period, work-from-home and other
            company policies. Pick a topic or type your own question below.</p>
        </div>
        <div class="suggest-title">Popular questions</div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for i, (icon, title, question) in enumerate(TOPICS):
        with cols[i % 2]:
            st.button(
                f"{icon}  {question}",
                key=f"suggest_{i}",
                on_click=queue_question,
                args=(question,),
                use_container_width=True,
            )


def render_history() -> None:
    for msg in st.session_state.messages:
        avatar = AVATAR_USER if msg["role"] == "user" else AVATAR_BOT
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])


# ----------------------------------------------------------------------------
# 7. MAIN APP
# ----------------------------------------------------------------------------
def main() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    init_session_state()
    render_sidebar()
    render_topbar()

    typed = st.chat_input("Type your HR question here...")
    prompt = typed or st.session_state.pending_question
    st.session_state.pending_question = None

    if not st.session_state.messages and not prompt:
        render_welcome()

    render_history()

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=AVATAR_USER):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=AVATAR_BOT):
            holder = st.empty()
            holder.markdown(TYPING_HTML, unsafe_allow_html=True)
            answer = get_answer(prompt)
            holder.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

    st.markdown(f'<div class="disclaimer">{DISCLAIMER}</div>', unsafe_allow_html=True)


main()