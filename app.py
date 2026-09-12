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
    page_title="AI Project Consultant",
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
                "Hello. I'm your AI Project Consultant. "
                "Tell me about your business or the project "
                "you have in mind, and I'll help you work "
                "through the requirements."
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
        background: #05090f !important;
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
                rgba(37, 99, 235, 0.22),
                transparent 62%
            ),
            radial-gradient(
                900px 700px at 92% 78%,
                rgba(6, 182, 212, 0.14),
                transparent 60%
            ),
            radial-gradient(
                700px 560px at 50% 22%,
                rgba(139, 92, 246, 0.10),
                transparent 68%
            ),
            #05090f !important;

        color: #eef6ff;
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

        border-bottom: 1px solid rgba(120, 185, 255, 0.14);

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
        color: #eaf6ff;

        background: linear-gradient(135deg, #2563eb, #06b6d4);
        box-shadow: 0 0 22px rgba(37, 130, 235, 0.35);
    }

    .brand-name {
        color: #f3f8ff;

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
        color: #8ba3ba;

        font-size: 0.82rem;
        font-weight: 500;

        transition: color 0.15s ease;
    }

    .nav-cta {
        color: #eaf6ff;

        padding: 9px 18px;

        border-radius: 999px;

        border: 1px solid rgba(70, 190, 255, 0.32);

        background: rgba(24, 110, 190, 0.16);
        backdrop-filter: blur(6px);

        box-shadow: 0 0 24px rgba(36, 150, 230, 0.10);
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

        color: #5fcaff;

        font-size: 0.72rem;
        font-weight: 700;

        letter-spacing: 0.24em;
        text-transform: uppercase;

        margin-bottom: 18px;

        padding: 6px 14px;
        border-radius: 999px;

        border: 1px solid rgba(80, 200, 255, 0.22);
        background: rgba(30, 130, 200, 0.08);
    }

    .eyebrow-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #4fd1a5;
        box-shadow: 0 0 8px rgba(79, 209, 165, 0.8);
    }

    .hero-title {
        color: #f5faff;

        font-size: clamp(2.6rem, 5.4vw, 4.7rem);

        font-weight: 800;

        line-height: 1.04;

        letter-spacing: -0.04em;

        margin: 0;
    }

    .hero-accent {
        background: linear-gradient(120deg, #4fb2ff, #22d3ee);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .hero-subtitle {
        max-width: 620px;

        margin: 20px auto 0 auto;

        color: #93aec6;

        font-size: clamp(0.94rem, 1.1vw, 1.06rem);

        line-height: 1.7;
    }


    /* ======================================================
       ROBOT
       ====================================================== */

    .robot-area {
        width: 100%;
        height: 236px;

        display: flex;

        align-items: center;
        justify-content: center;

        position: relative;

        margin: clamp(16px, 3vw, 28px) auto 0 auto;
    }

    .robot-glow {
        position: absolute;

        width: 220px;
        height: 120px;

        left: 50%;
        bottom: 26px;

        transform: translateX(-50%);

        border-radius: 50%;

        background: radial-gradient(
            ellipse,
            rgba(34, 211, 238, 0.26),
            rgba(59, 130, 246, 0.12),
            transparent 72%
        );

        filter: blur(28px);
        animation: robotPulse 4s ease-in-out infinite;
    }

    @keyframes robotPulse {
        0%, 100% { opacity: 0.75; transform: translateX(-50%) scale(1); }
        50% { opacity: 1; transform: translateX(-50%) scale(1.08); }
    }

    .robot-holder {
        width: 250px;
        height: 220px;

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

        background: linear-gradient(145deg, rgba(37,99,235,0.22), rgba(6,182,212,0.16));
        border: 1px solid rgba(103, 200, 255, 0.35);
        box-shadow: 0 0 40px rgba(45, 160, 230, 0.18);

        animation: chipFloat 3.4s ease-in-out infinite;
    }

    @keyframes chipFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }


    /* ======================================================
       WELCOME
       ====================================================== */

    .welcome {
        text-align: center;

        margin: 4px auto 28px auto;
    }

    .welcome-title {
        color: #f0f8ff;

        font-size: 1.1rem;
        font-weight: 650;

        margin-bottom: 6px;
    }

    .welcome-copy {
        max-width: 560px;

        margin: 0 auto;

        color: #8ca3ba;

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
        color: #6fc3ec;

        font-size: 0.68rem;
        font-weight: 700;

        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .chat-status {
        display: flex;
        align-items: center;
        gap: 7px;

        color: #7f96ad;

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

        border: 1px solid rgba(80, 190, 245, 0.20) !important;

        border-radius: 26px !important;

        background: linear-gradient(
            160deg,
            rgba(17, 41, 66, 0.92),
            rgba(7, 20, 35, 0.96)
        ) !important;

        backdrop-filter: blur(10px);

        box-shadow:
            0 34px 110px rgba(0, 0, 0, 0.38),
            0 0 60px rgba(25, 130, 220, 0.08) !important;

        padding: 16px !important;
    }


    /* ======================================================
       MESSAGE AREA
       ====================================================== */

    .st-key-chat_history {
        background: rgba(4, 13, 24, 0.35) !important;

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
        color: #e7f2fb !important;
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
        max-width: 84%;

        background: linear-gradient(
            135deg,
            rgba(14, 116, 150, 0.16),
            rgba(24, 90, 176, 0.10)
        );

        border-color: rgba(80, 205, 236, 0.16);
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
        max-width: 76%;

        background: linear-gradient(
            135deg,
            rgba(37, 99, 235, 0.30),
            rgba(99, 82, 235, 0.20)
        );

        border-color: rgba(96, 170, 255, 0.24);
        border-top-right-radius: 5px;
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
        color: #ffffff;
        font-weight: 700;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] a {
        color: #6fd3ff;
        text-decoration: underline;
        text-underline-offset: 2px;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] ul,
    .st-key-chat_history [data-testid="stMarkdownContainer"] ol {
        margin: 4px 0 8px 0;
        padding-left: 20px;
        color: #e7f2fb;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] li {
        margin-bottom: 4px;
        font-size: 0.92rem;
        line-height: 1.6;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] code {
        background: rgba(6, 18, 32, 0.75);
        border: 1px solid rgba(90, 190, 240, 0.18);
        color: #7fe0ff;
        border-radius: 5px;
        padding: 1px 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] pre {
        background: rgba(5, 14, 26, 0.85);
        border: 1px solid rgba(90, 190, 240, 0.18);
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

        border-left: 3px solid #f5b942;
        border-radius: 6px;

        background: rgba(245, 185, 66, 0.08);
        color: #f2dcb0;

        font-size: 0.88rem;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] hr {
        border-color: rgba(120, 185, 255, 0.14);
        margin: 10px 0;
    }

    /* Tables */
    .st-key-chat_history [data-testid="stMarkdownContainer"] table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;

        margin: 8px 0 4px 0;

        border: 1px solid rgba(90, 190, 240, 0.20);
        border-radius: 12px;
        overflow: hidden;

        font-size: 0.85rem;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] thead th {
        background: rgba(37, 99, 235, 0.22);
        color: #eaf6ff;
        font-weight: 700;
        text-align: left;
        padding: 9px 12px;
        border-bottom: 1px solid rgba(90, 190, 240, 0.20);
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] tbody td {
        padding: 9px 12px;
        color: #dcecf9;
        border-bottom: 1px solid rgba(90, 190, 240, 0.10);
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] tbody tr:last-child td {
        border-bottom: none;
    }

    .st-key-chat_history [data-testid="stMarkdownContainer"] tbody tr:nth-child(even) {
        background: rgba(90, 190, 240, 0.05);
    }


    /* ======================================================
       TYPING INDICATOR
       ====================================================== */

    .typing-dots {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 2px;
    }

    .typing-dots span {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #8fd6ff;
        animation: typingBounce 1.2s infinite ease-in-out;
    }

    .typing-dots span:nth-child(2) { animation-delay: 0.15s; }
    .typing-dots span:nth-child(3) { animation-delay: 0.3s; }

    @keyframes typingBounce {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
        30% { transform: translateY(-4px); opacity: 1; }
    }


    /* ======================================================
       INPUT
       ====================================================== */

    .st-key-chat_form {
        margin-top: 12px;
    }

    .st-key-chat_form input {
        height: 50px !important;

        background: rgba(5, 15, 27, 0.97) !important;

        color: #f2f8fd !important;

        border: 1px solid rgba(72, 177, 245, 0.24) !important;

        border-radius: 15px !important;

        font-size: 0.92rem !important;
    }

    .st-key-chat_form input:focus {
        border-color: rgba(95, 200, 255, 0.55) !important;
        box-shadow: 0 0 0 3px rgba(56, 170, 235, 0.14) !important;
    }

    .st-key-chat_form input::placeholder {
        color: #6c8398 !important;
    }

    .st-key-chat_form input:disabled {
        opacity: 0.55 !important;
    }

    .st-key-chat_form label {
        display: none !important;
    }


    /* ======================================================
       SEND BUTTON
       ====================================================== */

    .st-key-chat_form button {
        height: 50px !important;

        border-radius: 15px !important;

        color: #ffffff !important;
        font-weight: 600 !important;

        background: linear-gradient(135deg, #1687e8, #08a8bd) !important;

        border: 1px solid rgba(126, 226, 255, 0.28) !important;

        box-shadow: 0 8px 28px rgba(14, 137, 221, 0.24);

        transition: filter 0.15s ease, transform 0.1s ease;
    }

    .st-key-chat_form button:hover:not(:disabled) {
        filter: brightness(1.1);
    }

    .st-key-chat_form button:active:not(:disabled) {
        transform: scale(0.98);
    }

    .st-key-chat_form button:disabled {
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

        .nav-item:not(.nav-cta) {
            display: none;
        }

        .hero-title {
            font-size: 2.4rem;
        }

        .robot-area {
            height: 180px;
        }

        .robot-holder {
            width: 200px;
            height: 180px;
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
            max-width: 92%;
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
            <div class="nav-item">Services</div>
            <div class="nav-item">Process</div>
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
    <div class="hero">

        <div class="eyebrow">
            <span class="eyebrow-dot"></span>
            AI-powered consultation
        </div>

        <div class="hero-title">
            AI Project <span class="hero-accent">Consultant</span>
        </div>

        <div class="hero-subtitle">
            Turn your project idea into a clear scope,
            practical recommendation, and next steps.
        </div>

    </div>
    """
)


# ============================================================
# ROBOT
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
# ============================================================

if robot_animation:

    animation_json = json.dumps(robot_animation)

    st.html(
        f"""
        <div class="robot-area">

            <div class="robot-glow"></div>

            <div class="robot-holder" id="robot-holder">
                <div class="robot-fallback" id="robot-fallback">
                    <div class="robot-fallback-chip"></div>
                </div>
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


# ============================================================
# WELCOME (first-time empty state)
# ============================================================

if len(st.session_state.messages) == 1:

    st.html(
        """
        <div class="welcome">
            <div class="welcome-title">Let's talk about your project.</div>
            <div class="welcome-copy">
                Start with your business, your idea, or the problem
                you want to solve. I'll ask the relevant questions
                as we go.
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
                    '<div class="typing-dots"><span></span><span></span>'
                    '<span></span></div>',
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