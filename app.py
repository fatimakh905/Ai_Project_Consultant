import base64
import json
import uuid
from pathlib import Path

import streamlit as st

from src.agent import get_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ctrlaltcrew | AI Project Consultant",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

ROBOT_PATH = ASSETS_DIR / "robot_hello.json"
LOGO_PATH = ASSETS_DIR / "logo.png"


# ============================================================
# LOAD ASSETS
#
# These are cached with st.cache_data because app.py re-runs on
# every user interaction (every send, every rerun in the
# loading-state flow below). Without caching, the same 20KB+
# JSON animation file was being re-read from disk and
# re-parsed on every single rerun for no reason.
# ============================================================

@st.cache_data(show_spinner=False)
def load_robot():
    if not ROBOT_PATH.exists():
        return None

    try:
        with ROBOT_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print("Robot error:", error)
        return None


@st.cache_data(show_spinner=False)
def load_logo():
    if not LOGO_PATH.exists():
        return None

    try:
        encoded = base64.b64encode(
            LOGO_PATH.read_bytes()
        ).decode("utf-8")

        suffix = LOGO_PATH.suffix.lower()

        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }.get(suffix, "image/png")

        return f"data:{mime};base64,{encoded}"

    except OSError as error:
        print("Logo error:", error)
        return None


robot_animation = load_robot()
logo_data = load_logo()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Welcome to ctrlaltcrew's project consultation. "
                "Tell me about your business, the problem you're trying "
                "to solve, or the product you want to build. "
                "I'll help you shape the requirements and find the right solution."
            ),
        }
    ]

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "agent" not in st.session_state:
    st.session_state.agent = get_agent()

# "pending" drives the two-step send flow: the user's message is
# appended and shown immediately, then a follow-up rerun performs
# the (blocking) agent call while a typing indicator is visible.
# This also prevents duplicate submissions while a reply is in
# flight, since the input/button are disabled whenever pending.
if "pending" not in st.session_state:
    st.session_state.pending = False

if "pending_message" not in st.session_state:
    st.session_state.pending_message = None


# ============================================================
# GLOBAL CSS
# ============================================================

st.html(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ======================================================
       GLOBAL PAGE
       ====================================================== */

    html,
    body {
        margin: 0 !important;
        padding: 0 !important;
        background: #f7f9fc !important;
    }

    .stApp,
    .stApp * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont,
            'Segoe UI', sans-serif;
    }

    .stApp {
        min-height: 100vh;

        background:
            radial-gradient(
                1100px 720px at 10% 0%,
                rgba(37, 99, 235, 0.07),
                transparent 62%
            ),
            radial-gradient(
                900px 700px at 92% 78%,
                rgba(6, 182, 212, 0.05),
                transparent 60%
            ),
            radial-gradient(
                700px 560px at 50% 22%,
                rgba(139, 92, 246, 0.04),
                transparent 68%
            ),
            #f7f9fc !important;

        color: #1e293b;
    }


    /* ======================================================
       REMOVE STREAMLIT CHROME
       ====================================================== */

    #MainMenu {
        display: none !important;
    }

    footer {
        display: none !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
    }

    /* Streamlit Community Cloud's own toolbar (Deploy button,
       status widget, top decoration bar) lives outside
       stHeader, so hiding stHeader alone does not remove it. */
    [data-testid="stToolbar"],
    [data-testid="stAppDeployButton"],
    [data-testid="stStatusWidget"],
    [data-testid="stDecoration"] {
        display: none !important;
    }


    /* ======================================================
       PAGE WIDTH / RHYTHM
       ====================================================== */

    .block-container {
        max-width: 1180px !important;

        padding-top: clamp(20px, 3vw, 44px) !important;
        padding-bottom: 56px !important;

        padding-left: clamp(20px, 3vw, 40px) !important;
        padding-right: clamp(20px, 3vw, 40px) !important;
    }


    /* ======================================================
       HEADER
       ====================================================== */

    .site-header {
        height: 76px;

        display: flex;
        align-items: center;
        justify-content: space-between;

        border-bottom: 1px solid rgba(15, 23, 42, 0.08);

        margin-bottom: clamp(40px, 6vw, 72px);
    }

    .brand-area {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-logo {
        width: 34px;
        height: 34px;

        object-fit: contain;
        border-radius: 9px;
    }

    .brand-mark {
        width: 34px;
        height: 34px;
        border-radius: 9px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 0.8rem;
        font-weight: 800;
        color: #ffffff;

        background: linear-gradient(135deg, #2563eb, #06b6d4);
        box-shadow: 0 4px 16px rgba(37, 130, 235, 0.28);
    }

    .brand-name {
        color: #0f172a;

        font-size: 1.02rem;
        font-weight: 700;

        letter-spacing: -0.01em;
    }

    .nav-area {
        display: flex;
        align-items: center;
        gap: 30px;
    }

    .nav-item {
        color: #64748b;

        font-size: 0.82rem;
        font-weight: 500;

        transition: color 0.15s ease;
    }

    .nav-cta {
        color: #1d4ed8;

        padding: 9px 18px;

        border-radius: 999px;

        border: 1px solid rgba(37, 99, 235, 0.30);

        background: rgba(37, 99, 235, 0.06);

        box-shadow: none;
    }


    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        text-align: center;
        padding: 0 12px;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;

        color: #2563eb;

        font-size: 0.72rem;
        font-weight: 700;

        letter-spacing: 0.24em;
        text-transform: uppercase;

        margin-bottom: 18px;

        padding: 6px 14px;
        border-radius: 999px;

        border: 1px solid rgba(37, 99, 235, 0.22);
        background: rgba(37, 99, 235, 0.05);
    }

    .eyebrow-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 6px rgba(16, 185, 129, 0.6);
    }

    .hero-title {
        color: #0f172a;

        font-size: clamp(2.6rem, 5.4vw, 4.7rem);

        font-weight: 800;

        line-height: 1.04;

        letter-spacing: -0.04em;

        margin: 0;
    }

    .hero-accent {
        background: linear-gradient(120deg, #2563eb, #0891b2);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .hero-subtitle {
        max-width: 620px;

        margin: 20px auto 0 auto;

        color: #55677c;

        font-size: clamp(0.94rem, 1.1vw, 1.06rem);

        line-height: 1.7;
    }


    /* ======================================================
       INTRO ROW (robot + welcome text, side by side)
       ====================================================== */

    .intro-row {
        display: flex;
        align-items: center;
        justify-content: center;

        gap: clamp(20px, 4vw, 44px);

        max-width: 720px;

        margin: clamp(20px, 4vw, 36px) auto 32px auto;
    }

    .robot-area {
        width: 190px;
        height: 190px;

        flex-shrink: 0;

        display: flex;

        align-items: center;
        justify-content: center;

        position: relative;
    }

    .robot-glow {
        position: absolute;

        width: 170px;
        height: 100px;

        left: 50%;
        bottom: 14px;

        transform: translateX(-50%);

        border-radius: 50%;

        background: radial-gradient(
            ellipse,
            rgba(34, 211, 238, 0.18),
            rgba(59, 130, 246, 0.10),
            transparent 72%
        );

        filter: blur(20px);
        animation: robotPulse 4s ease-in-out infinite;
    }

    @keyframes robotPulse {
        0%, 100% { opacity: 0.7; transform: translateX(-50%) scale(1); }
        50% { opacity: 1; transform: translateX(-50%) scale(1.08); }
    }

    .robot-holder {
        width: 190px;
        height: 180px;

        position: relative;
        z-index: 2;
    }

    /* Instant fallback shown before/if the Lottie animation
       loads, so the hero never shows a blank hole. */
    .robot-fallback {
        position: absolute;
        inset: 0;

        display: flex;
        align-items: center;
        justify-content: center;
    }

    .robot-fallback-chip {
        width: 96px;
        height: 96px;
        border-radius: 26px;

        display: flex;
        align-items: center;
        justify-content: center;

        background: linear-gradient(145deg, #2563eb, #06b6d4);
        border: 1px solid rgba(37, 99, 235, 0.25);
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.22);

        animation: chipFloat 3.4s ease-in-out infinite;
    }

    @keyframes chipFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }


    /* ======================================================
       WELCOME TEXT (right side of the intro row)
       ====================================================== */

    .welcome {
        text-align: left;
        flex: 1;
        min-width: 0;
    }

    .welcome-title {
        color: #0f172a;

        font-size: 1.1rem;
        font-weight: 650;

        margin-bottom: 6px;
    }

    .welcome-copy {
        color: #5b6b7f;

        font-size: 0.86rem;

        line-height: 1.65;
    }


    /* ======================================================
       CHAT LABEL
       ====================================================== */

    .chat-heading {
        display: flex;

        justify-content: space-between;
        align-items: center;

        margin: 0 6px 10px 6px;
    }

    .chat-label {
        color: #2563eb;

        font-size: 0.68rem;
        font-weight: 700;

        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .chat-status {
        display: flex;
        align-items: center;
        gap: 7px;

        color: #7c8ba0;

        font-size: 0.68rem;
    }

    .status-dot {
        width: 6px;
        height: 6px;

        border-radius: 50%;

        background: #57d59a;
        box-shadow: 0 0 6px rgba(87, 213, 154, 0.8);
    }

    .status-dot.busy {
        background: #f5b942;
        box-shadow: 0 0 6px rgba(245, 185, 66, 0.8);
        animation: dotBlink 1s ease-in-out infinite;
    }

    @keyframes dotBlink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.35; }
    }


    /* ======================================================
       CHAT SHELL
       ====================================================== */

    .st-key-chat_shell {
        max-width: 900px;
        margin: 0 auto;

        border: 1px solid rgba(15, 23, 42, 0.08) !important;

        border-radius: 26px !important;

        background: #ffffff !important;

        box-shadow:
            0 24px 70px rgba(15, 23, 42, 0.08),
            0 2px 10px rgba(15, 23, 42, 0.04) !important;

        padding: 16px !important;
    }


    /* ======================================================
       MESSAGE AREA
       ====================================================== */

    .st-key-chat_history {
        background: #f5f7fa !important;

        border-radius: 18px !important;

        padding: 14px 10px !important;
    }

    .st-key-chat_history [data-testid="stVerticalBlock"] {
        gap: 0.35rem;
    }


    /* ======================================================
       MESSAGE BUBBLES
       ====================================================== */

    .st-key-chat_history [data-testid="stChatMessage"] {
        margin: 6px 2px;
        padding: 0;
        background: transparent;
        border: none;
    }

    /* Hide default avatars entirely - we rely on bubble side +
       color instead of icons for role distinction. */
    .st-key-chat_history [data-testid="stChatMessageAvatarUser"],
    .st-key-chat_history [data-testid="stChatMessageAvatarAssistant"],
    .st-key-chat_history [data-testid="stChatMessageAvatarCustom"] {
        display: none !important;
    }

    .st-key-chat_history [data-testid="stChatMessageContent"] {
        border-radius: 16px;
        padding: 12px 16px;
        border: 1px solid transparent;
    }

    .st-key-chat_history [data-testid="stChatMessageContent"] p {
        color: #1e293b !important;
        font-size: 0.93rem !important;
        line-height: 1.68 !important;
        margin: 0 0 8px 0 !important;
    }

    .st-key-chat_history [data-testid="stChatMessageContent"] p:last-child {
        margin-bottom: 0 !important;
    }

    /* Assistant: left-aligned bubble */
    .st-key-chat_history [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarAssistant"]
    ) {
        display: flex;
        justify-content: flex-start;
    }

    .st-key-chat_history [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarAssistant"]
    ) [data-testid="stChatMessageContent"] {
        /* !important + width:fit-content because Streamlit sets
           its own width on this element that otherwise beats a
           plain max-width and defeats the flex alignment above. */
        width: fit-content !important;
        max-width: 84% !important;
        margin-right: auto !important;
        margin-left: 0 !important;

        background: #eef4fb;

        border-color: rgba(37, 99, 235, 0.12);
        border-top-left-radius: 5px;
    }

    /* User: right-aligned bubble */
    .st-key-chat_history [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) {
        display: flex;
        justify-content: flex-end;
    }

    .st-key-chat_history [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) [data-testid="stChatMessageContent"] {
        width: fit-content !important;
        max-width: 76% !important;
        margin-left: auto !important;
        margin-right: 0 !important;

        background: linear-gradient(135deg, #2563eb, #0891b2);

        border-color: transparent;
        border-top-right-radius: 5px;
    }

    /* The gradient user bubble needs light text; everything
       else in the message area defaults to dark text above. */
    .st-key-chat_history [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) [data-testid="stChatMessageContent"] p {
        color: #ffffff !important;
    }

    /* If a user message happens to contain markdown (bold, links,
       lists), keep it readable against the solid gradient bubble
       instead of inheriting the dark-on-light defaults below. */
    .st-key-chat_history [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) [data-testid="stMarkdownContainer"] strong,
    .st-key-chat_history [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) [data-testid="stMarkdownContainer"] li,
    .st-key-chat_history [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) [data-testid="stMarkdownContainer"] ul,
    .st-key-chat_history [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) [data-testid="stMarkdownContainer"] ol {
        color: #ffffff !important;
    }

    .st-key-chat_history [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) [data-testid="stMarkdownContainer"] a {
        color: #e0f2ff !important;
    }


    /* ======================================================
       MARKDOWN CONTENT INSIDE MESSAGES
       (tables, code, lists, links, blockquotes)
       ====================================================== */

    .st-key-chat_history [data-testid="stMarkdownContainer"] {
        width: 100%;
        overflow-x: auto;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] strong {
        color: #0f172a;
        font-weight: 700;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] a {
        color: #1d4ed8;
        text-decoration: underline;
        text-underline-offset: 2px;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] ul,
    .st-key-chat_history [data-testid="stMarkdownContainer"] ol {
        margin: 4px 0 8px 0;
        padding-left: 20px;
        color: #1e293b;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] li {
        margin-bottom: 4px;
        font-size: 0.92rem;
        line-height: 1.6;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] code {
        background: rgba(15, 23, 42, 0.06);
        border: 1px solid rgba(15, 23, 42, 0.10);
        color: #0e7490;
        border-radius: 5px;
        padding: 1px 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] pre {
        background: #f1f5f9;
        border: 1px solid rgba(15, 23, 42, 0.10);
        border-radius: 12px;
        padding: 12px 14px;
        overflow-x: auto;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] pre code {
        background: transparent;
        border: none;
        padding: 0;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] blockquote {
        margin: 6px 0;
        padding: 8px 14px;

        border-left: 3px solid #d97706;
        border-radius: 6px;

        background: rgba(217, 119, 6, 0.08);
        color: #7c4a05;

        font-size: 0.88rem;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] hr {
        border-color: rgba(15, 23, 42, 0.10);
        margin: 10px 0;
    }

    /* Tables */
    .st-key-chat_history [data-testid="stMarkdownContainer"] table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;

        margin: 8px 0 4px 0;

        border: 1px solid rgba(15, 23, 42, 0.10);
        border-radius: 12px;
        overflow: hidden;

        font-size: 0.85rem;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] thead th {
        background: rgba(37, 99, 235, 0.10);
        color: #0f172a;
        font-weight: 700;
        text-align: left;
        padding: 9px 12px;
        border-bottom: 1px solid rgba(15, 23, 42, 0.10);
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] tbody td {
        padding: 9px 12px;
        color: #334155;
        border-bottom: 1px solid rgba(15, 23, 42, 0.06);
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] tbody tr:last-child td {
        border-bottom: none;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] tbody tr:nth-child(even) {
        background: rgba(15, 23, 42, 0.02);
    }


    /* ======================================================
       TYPING INDICATOR
       ====================================================== */

    .typing-indicator {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 2px 2px;
    }

    .typing-indicator-label {
        color: #9fc3dd;
        font-size: 0.86rem;
    }

    .typing-dots {
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .typing-dots span {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #4fd1e8;
        box-shadow: 0 0 8px rgba(79, 209, 232, 0.7);
        animation: typingBounce 1.1s infinite ease-in-out;
    }

    .typing-dots span:nth-child(2) { animation-delay: 0.16s; }
    .typing-dots span:nth-child(3) { animation-delay: 0.32s; }

    @keyframes typingBounce {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.45; }
        30% { transform: translateY(-6px); opacity: 1; }
    }


    /* ======================================================
       INPUT
       ====================================================== */

    [data-testid="stForm"] {
        margin-top: 12px;
    }

    [data-testid="stForm"] input {
        height: 50px !important;

        background: rgba(5, 15, 27, 0.97) !important;

        color: #f2f8fd !important;

        border: 1px solid rgba(72, 177, 245, 0.24) !important;

        border-radius: 15px !important;

        font-size: 0.92rem !important;
    }

    [data-testid="stForm"] input:focus {
        border-color: rgba(95, 200, 255, 0.55) !important;
        box-shadow: 0 0 0 3px rgba(56, 170, 235, 0.14) !important;
    }

    [data-testid="stForm"] input::placeholder {
        color: #6c8398 !important;
    }

    [data-testid="stForm"] input:disabled {
        opacity: 0.55 !important;
    }

    [data-testid="stForm"] label {
        display: none !important;
    }


    /* ======================================================
       SEND BUTTON
       ====================================================== */

    [data-testid="stForm"] button {
        height: 50px !important;

        border-radius: 15px !important;

        color: #ffffff !important;
        font-weight: 600 !important;

        background: linear-gradient(135deg, #1687e8, #08a8bd) !important;

        border: 1px solid rgba(126, 226, 255, 0.28) !important;

        box-shadow: 0 8px 28px rgba(14, 137, 221, 0.24);

        transition: filter 0.15s ease, transform 0.1s ease;
    }

    [data-testid="stForm"] button:hover:not(:disabled) {
        filter: brightness(1.1);
    }

    [data-testid="stForm"] button:active:not(:disabled) {
        transform: scale(0.98);
    }

    [data-testid="stForm"] button:disabled {
        opacity: 0.55 !important;
        filter: grayscale(0.3);
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;

        margin-top: 22px;

        color: #5c7690;

        font-size: 0.66rem;

        letter-spacing: 0.05em;
    }


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 720px) {

        .block-container {
            padding-left: 16px !important;
            padding-right: 16px !important;
        }

        .site-header {
            height: 64px;
            margin-bottom: 30px;
        }

        .hero-title {
            font-size: 2.4rem;
        }

        .intro-row {
            flex-direction: column;
            text-align: center;
            gap: 14px;
        }

        .welcome {
            text-align: center;
        }

        .robot-area {
            width: 160px;
            height: 160px;
        }

        .robot-holder {
            width: 160px;
            height: 150px;
        }

        .st-key-chat_shell {
            padding: 10px !important;
            border-radius: 20px !important;
        }

        .st-key-chat_history {
            height: 400px !important;
        }

        .st-key-chat_history [data-testid="stChatMessage"]:has(
            [data-testid="stChatMessageAvatarAssistant"]
        ) [data-testid="stChatMessageContent"],
        .st-key-chat_history [data-testid="stChatMessage"]:has(
            [data-testid="stChatMessageAvatarUser"]
        ) [data-testid="stChatMessageContent"] {
            max-width: 92% !important;
        }
    }

    </style>
    """
)


# ============================================================
# HEADER
# ============================================================

if logo_data:
    brand_mark_html = f'<img src="{logo_data}" class="brand-logo" alt="logo" />'
else:
    brand_mark_html = '<div class="brand-mark">CC</div>'

st.html(
    f"""
    <div class="site-header">

        <div class="brand-area">
            {brand_mark_html}
            <div class="brand-name">ctrlaltcrew</div>
        </div>

        <div class="nav-area">
            <div class="nav-item nav-cta">Start a Project</div>
        </div>

    </div>
    """
)


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="eyebrow">
    <span class="eyebrow-dot"></span>
    START A PROJECT WITH CTRLALTcrew
</div>

<div class="hero-title">
    Let's build something <span class="hero-accent">useful.</span>
</div>

<div class="hero-subtitle">
    Tell us what you're trying to build. Our AI Project Consultant
    will help you define the right solution, scope the project,
    and understand the next steps.
</div>

    
    """
)


# ============================================================
# INTRO ROW: ROBOT + WELCOME TEXT (side by side)
#
# Root cause of the animation not rendering: the previous
# implementation injected a `<script src="...lottie.min.js">`
# tag and then, in a second inline <script>, immediately called
# `lottie.loadAnimation(...)`. Dynamically inserted `<script
# src="...">` tags load asynchronously by default, so the second
# script frequently ran before the library had finished
# downloading, silently no-op'd (`if (!window.lottie) return;`),
# and nothing ever appeared.
#
# Fix: create the script element manually, wait for its `onload`
# event before touching `window.lottie`, cache the loaded
# library on `window` so we don't re-fetch it on every Streamlit
# rerun (the whole block re-renders on every chat turn), and
# destroy any previous animation instance before creating a new
# one so reruns don't leak animation frames. A lightweight CSS
# fallback chip is shown immediately so there is never a blank
# gap even before the library loads or if it fails outright.
#
# The welcome text now always sits next to the robot (instead of
# only appearing before the first message) so the layout doesn't
# go lopsided once the conversation starts.
# ============================================================

if robot_animation:

    animation_json = json.dumps(robot_animation)

    st.html(
        f"""
        <div class="intro-row">

            <div class="robot-area">

                <div class="robot-glow"></div>

                <div class="robot-holder" id="robot-holder">
                    <div class="robot-fallback" id="robot-fallback">
                        <div class="robot-fallback-chip"></div>
                    </div>
                </div>

            </div>

            <div class="welcome-title">
    Start your project conversation.
</div>

<div class="welcome-copy">
    Share your business, idea, or the problem you want to solve.
    We'll ask the right questions and help you figure out what
    to build next.
</div>

        </div>

        <script>
        (function() {{
            var ANIMATION_DATA = {animation_json};

            function renderAnimation() {{
                var container = document.getElementById("robot-holder");
                if (!container || !window.lottie) {{
                    return;
                }}

                if (window.__robotAnimInstance) {{
                    try {{ window.__robotAnimInstance.destroy(); }} catch (e) {{}}
                }}

                var fallback = document.getElementById("robot-fallback");
                if (fallback) {{
                    fallback.style.display = "none";
                }}

                try {{
                    window.__robotAnimInstance = window.lottie.loadAnimation({{
                        container: container,
                        renderer: "svg",
                        loop: true,
                        autoplay: true,
                        animationData: ANIMATION_DATA
                    }});
                }} catch (e) {{
                    console.error("Robot animation failed to render:", e);
                }}
            }}

            if (window.lottie) {{
                renderAnimation();
                return;
            }}

            if (!window.__lottieLoadPromise) {{
                window.__lottieLoadPromise = new Promise(function(resolve, reject) {{
                    var script = document.createElement("script");
                    script.src = "https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js";
                    script.onload = resolve;
                    script.onerror = reject;
                    document.head.appendChild(script);
                }});
            }}

            window.__lottieLoadPromise.then(renderAnimation).catch(function(error) {{
                console.error("Failed to load lottie-web:", error);
            }});
        }})();
        </script>
        """,
        unsafe_allow_javascript=True,
    )

else:

    # No animation file found - still show the welcome text next to
    # the static fallback chip so the layout never depends on the
    # asset being present.
    st.html(
        """
        <div class="intro-row">

            <div class="robot-area">
                <div class="robot-glow"></div>
                <div class="robot-holder">
                    <div class="robot-fallback">
                        <div class="robot-fallback-chip"></div>
                    </div>
                </div>
            </div>

            <div class="welcome">
                <div class="welcome-title">Let's talk about your project.</div>
                <div class="welcome-copy">
                    Start with your business, your idea, or the problem
                    you want to solve. I'll ask the relevant questions
                    as we go.
                </div>
            </div>

        </div>
        """
    )


# ============================================================
# CHAT HEADING
# ============================================================

status_dot_class = "status-dot busy" if st.session_state.pending else "status-dot"
status_label = "Thinking..." if st.session_state.pending else "AI consultant online"

st.html(
    f"""
    <div class="chat-heading">
        <div class="chat-label">Project consultation</div>
        <div class="chat-status">
            <div class="{status_dot_class}"></div>
            {status_label}
        </div>
    </div>
    """
)


# ============================================================
# CHAT SHELL
# ============================================================

with st.container(border=True, key="chat_shell"):

    # --------------------------------------------------------
    # MESSAGE AREA
    # --------------------------------------------------------

    with st.container(height=520, border=False, key="chat_history"):

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if st.session_state.pending:
            with st.chat_message("assistant"):
                st.markdown(
                    '<div class="typing-indicator">'
                    '<span class="typing-indicator-label">Thinking</span>'
                    '<div class="typing-dots">'
                    '<span></span><span></span><span></span>'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    with st.form(key="chat_form", clear_on_submit=True):

        input_col, button_col = st.columns([8.4, 1.6], gap="small")

        with input_col:
            user_input = st.text_input(
                "Message",
                placeholder="Tell me about your project...",
                label_visibility="collapsed",
                disabled=st.session_state.pending,
            )

        with button_col:
            submitted = st.form_submit_button(
                "Send",
                use_container_width=True,
                disabled=st.session_state.pending,
            )


# ============================================================
# PROCESS MESSAGE
#
# Two-step flow so the UI can show the user's message and a
# typing indicator *before* the (blocking) agent call runs:
#
#   1. On submit: append the user message, mark pending, rerun.
#      This rerun renders the message list (including the new
#      user bubble and the typing indicator) before this script
#      reaches step 2 below.
#   2. On the next run, since pending is already True, call the
#      agent, append the reply, clear pending, and rerun once
#      more to reveal the final state.
#
# This also removes a real bug in the original single-step flow:
# nothing disabled the input/button between click and response,
# so a fast double-click could fire two overlapping agent calls
# against the same thread_id.
# ============================================================

if submitted and user_input.strip() and not st.session_state.pending:

    st.session_state.messages.append(
        {"role": "user", "content": user_input.strip()}
    )
    st.session_state.pending_message = user_input.strip()
    st.session_state.pending = True

    st.rerun()


if st.session_state.pending:

    user_message = st.session_state.pending_message

    try:
        response = st.session_state.agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            },
            config={
                "configurable": {
                    "thread_id": st.session_state.thread_id
                }
            },
        )

        assistant_response = response["messages"][-1].content

    except Exception as error:

        print("Agent error:", error)

        assistant_response = (
            "> **Connection issue.** I'm having trouble reaching "
            "the AI service right now. Please try again in a moment."
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )

    st.session_state.pending = False
    st.session_state.pending_message = None

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">
        ctrlaltcrew · AI Project Consultant
    </div>
    """
)