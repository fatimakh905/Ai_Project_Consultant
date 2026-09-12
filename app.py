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
# ============================================================

def load_robot():
    if not ROBOT_PATH.exists():
        return None

    try:
        with ROBOT_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print("Robot error:", error)
        return None


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
                "Hello. I’m your AI Project Consultant. "
                "Tell me about your business or the project "
                "you have in mind, and I’ll help you work "
                "through the requirements."
            ),
        }
    ]

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "agent" not in st.session_state:
    st.session_state.agent = get_agent()


# ============================================================
# GLOBAL CSS
# ============================================================

st.html(
    """
    <style>

    /* ======================================================
       GLOBAL PAGE
       ====================================================== */

    html,
    body {
        margin: 0 !important;
        padding: 0 !important;
        background: #071321 !important;
    }

    .stApp {
        min-height: 100vh;

        background:
            radial-gradient(
                900px 620px at 8% 8%,
                rgba(30, 92, 190, 0.24),
                transparent 66%
            ),
            radial-gradient(
                800px 620px at 92% 80%,
                rgba(7, 181, 207, 0.14),
                transparent 65%
            ),
            radial-gradient(
                550px 450px at 53% 26%,
                rgba(91, 73, 192, 0.10),
                transparent 72%
            ),
            #071321 !important;

        color: #eef7ff;
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

    header {
        background: transparent !important;
    }


    /* ======================================================
       PAGE WIDTH
       ====================================================== */

    .block-container {
        max-width: 1120px !important;

        padding-top: 0 !important;
        padding-bottom: 60px !important;

        padding-left: 28px !important;
        padding-right: 28px !important;
    }


    /* ======================================================
       HEADER
       ====================================================== */

    .site-header {
        height: 70px;

        display: flex;
        align-items: center;
        justify-content: space-between;

        border-bottom:
            1px solid rgba(118, 183, 255, 0.12);

        margin-bottom: 48px;
    }

    .brand-area {
        display: flex;
        align-items: center;
        gap: 11px;
    }

    .brand-logo {
        width: 32px;
        height: 32px;

        object-fit: contain;
        border-radius: 8px;
    }

    .brand-name {
        color: #edf6ff;

        font-size: 0.96rem;
        font-weight: 650;

        letter-spacing: -0.015em;
    }

    .nav-area {
        display: flex;
        align-items: center;
        gap: 26px;
    }

    .nav-item {
        color: #829bb3;

        font-size: 0.76rem;
        font-weight: 500;
    }

    .nav-cta {
        color: #e5f5ff;

        padding: 8px 15px;

        border-radius: 999px;

        border:
            1px solid rgba(60, 185, 255, 0.28);

        background:
            rgba(18, 104, 180, 0.13);

        box-shadow:
            0 0 22px rgba(36, 150, 230, 0.08);
    }


    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        text-align: center;
    }

    .eyebrow {
        color: #55c8ff;

        font-size: 0.67rem;
        font-weight: 650;

        letter-spacing: 0.23em;
        text-transform: uppercase;

        margin-bottom: 14px;
    }

    .hero-title {
        color: #f4f9ff;

        font-size: clamp(
            2.8rem,
            5vw,
            4.5rem
        );

        font-weight: 760;

        line-height: 1;

        letter-spacing: -0.06em;

        margin: 0;
    }

    .hero-accent {
        color: #48b9ff;
    }

    .hero-subtitle {
        max-width: 620px;

        margin:
            17px auto 0 auto;

        color: #8ba8c2;

        font-size: 0.94rem;

        line-height: 1.65;
    }


    /* ======================================================
       ROBOT
       ====================================================== */

    .robot-area {
        width: 100%;

        height: 220px;

        display: flex;

        align-items: center;
        justify-content: center;

        position: relative;

        margin:
            2px auto 0 auto;
    }

    .robot-glow {
        position: absolute;

        width: 190px;
        height: 100px;

        left: 50%;
        bottom: 24px;

        transform: translateX(-50%);

        border-radius: 50%;

        background:
            radial-gradient(
                ellipse,
                rgba(29, 194, 231, 0.24),
                rgba(44, 113, 244, 0.10),
                transparent 72%
            );

        filter: blur(25px);
    }

    .robot-holder {
        width: 245px;
        height: 215px;

        position: relative;

        z-index: 2;
    }


    /* ======================================================
       WELCOME
       ====================================================== */

    .welcome {
        text-align: center;

        margin:
            0 auto 25px auto;
    }

    .welcome-title {
        color: #eff7ff;

        font-size: 1.08rem;
        font-weight: 620;

        margin-bottom: 5px;
    }

    .welcome-copy {
        max-width: 560px;

        margin: 0 auto;

        color: #839cb5;

        font-size: 0.82rem;

        line-height: 1.6;
    }


    /* ======================================================
       CHAT LABEL
       ====================================================== */

    .chat-heading {
        display: flex;

        justify-content: space-between;
        align-items: center;

        margin:
            0 4px 9px 4px;
    }

    .chat-label {
        color: #67bde9;

        font-size: 0.66rem;
        font-weight: 650;

        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    .chat-status {
        display: flex;
        align-items: center;
        gap: 6px;

        color: #7592aa;

        font-size: 0.64rem;
    }

    .status-dot {
        width: 6px;
        height: 6px;

        border-radius: 50%;

        background: #57d59a;
    }


    /* ======================================================
       CHAT SHELL
       ====================================================== */

    .st-key-chat_shell {
        border:
            1px solid rgba(73, 181, 245, 0.20) !important;

        border-radius: 24px !important;

        background:
            linear-gradient(
                145deg,
                rgba(16, 39, 63, 0.94),
                rgba(8, 24, 41, 0.96)
            ) !important;

        box-shadow:
            0 30px 100px rgba(0, 0, 0, 0.34),
            0 0 55px rgba(25, 130, 220, 0.07) !important;

        padding: 14px !important;
    }


    /* ======================================================
       MESSAGE AREA
       ====================================================== */

    .st-key-chat_history {
        background:
            rgba(4, 15, 27, 0.30) !important;

        border-radius: 17px !important;

        padding: 8px !important;
    }


    /* ======================================================
       MESSAGES
       ====================================================== */

    .st-key-chat_history [data-testid="stChatMessage"] {
        border-radius: 17px;

        margin:
            7px 2px;

        padding:
            10px 14px;

        border:
            1px solid transparent;
    }

    .st-key-chat_history
    [data-testid="stChatMessage"] p {
        color: #e3f0fa !important;

        font-size: 0.91rem !important;

        line-height: 1.68 !important;
    }


    /* Assistant */

    .st-key-chat_history
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background:
            linear-gradient(
                135deg,
                rgba(12, 121, 155, 0.12),
                rgba(25, 89, 174, 0.08)
            );

        border-color:
            rgba(75, 201, 236, 0.12);
    }


    /* User */

    .st-key-chat_history
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background:
            linear-gradient(
                135deg,
                rgba(37, 99, 235, 0.20),
                rgba(79, 70, 229, 0.14)
            );

        border-color:
            rgba(72, 168, 255, 0.18);
    }


    /* Hide default avatars */

    .st-key-chat_history
    [data-testid="stChatMessageAvatarUser"],
    .st-key-chat_history
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }


    /* ======================================================
       INPUT
       ====================================================== */

    .st-key-chat_form {
        margin-top: 10px;
    }

    .st-key-chat_form input {
        height: 48px !important;

        background:
            rgba(5, 17, 30, 0.97) !important;

        color: #f2f8fd !important;

        border:
            1px solid rgba(72, 177, 245, 0.23) !important;

        border-radius: 15px !important;

        font-size: 0.90rem !important;

        box-shadow:
            inset 0 0 0 1px
            rgba(45, 160, 229, 0.025);
    }

    .st-key-chat_form input::placeholder {
        color: #68839c !important;
    }

    .st-key-chat_form label {
        display: none !important;
    }


    /* ======================================================
       SEND BUTTON
       ====================================================== */

    .st-key-chat_form button {
        height: 48px !important;

        border-radius: 15px !important;

        color: #ffffff !important;

        background:
            linear-gradient(
                135deg,
                #1687e8,
                #08a8bd
            ) !important;

        border:
            1px solid rgba(126, 226, 255, 0.28) !important;

        box-shadow:
            0 8px 28px
            rgba(14, 137, 221, 0.24);
    }

    .st-key-chat_form button:hover {
        filter: brightness(1.09);
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;

        margin-top: 17px;

        color: #55718a;

        font-size: 0.64rem;

        letter-spacing: 0.05em;
    }


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 720px) {

        .block-container {
            padding-left: 14px !important;
            padding-right: 14px !important;
        }

        .site-header {
            margin-bottom: 34px;
        }

        .nav-item:not(.nav-cta) {
            display: none;
        }

        .hero-title {
            font-size: 2.55rem;
        }

        .robot-area {
            height: 190px;
        }

        .robot-holder {
            width: 215px;
            height: 190px;
        }

        .st-key-chat_shell {
            padding: 10px !important;
        }
    }

    </style>
    """
)


# ============================================================
# HEADER
# ============================================================

if logo_data:
    logo_html = f"""
        <img
            src="{logo_data}"
            class="brand-logo"
            alt="logo"
        />
    """
else:
    logo_html = ""


st.html(
    f"""
    <div class="site-header">

        <div class="brand-area">

            {logo_html}

            <div class="brand-name">
                ctrlaltcrew
            </div>

        </div>

        <div class="nav-area">

            <div class="nav-item">
                Services
            </div>

            <div class="nav-item">
                Process
            </div>

            <div class="nav-item nav-cta">
                Start a Project
            </div>

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
# ============================================================

if robot_animation:

    animation_data = json.dumps(robot_animation)

    st.html(
        f"""
        <div class="robot-area">

            <div class="robot-glow"></div>

            <div class="robot-holder"
                 id="robot-holder">
            </div>

        </div>

        <script
            src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js">
        </script>

        <script>

        (() => {{

            const container =
                document.getElementById("robot-holder");

            if (!container || !window.lottie) {{
                return;
            }}

            const animationData = {animation_data};

            lottie.loadAnimation({{
                container: container,
                renderer: "svg",
                loop: true,
                autoplay: true,
                animationData: animationData
            }});

        }})();

        </script>
        """,
        unsafe_allow_javascript=True,
    )


# ============================================================
# WELCOME
# ============================================================

if len(st.session_state.messages) == 1:

    st.html(
        """
        <div class="welcome">

            <div class="welcome-title">
                Let's talk about your project.
            </div>

            <div class="welcome-copy">
                Start with your business, your idea, or the problem
                you want to solve. I’ll ask the relevant questions
                as we go.
            </div>

        </div>
        """
    )


# ============================================================
# CHAT HEADER
# ============================================================

st.html(
    """
    <div class="chat-heading">

        <div class="chat-label">
            Project consultation
        </div>

        <div class="chat-status">
            <div class="status-dot"></div>
            AI consultant online
        </div>

    </div>
    """
)


# ============================================================
# CHAT SHELL
# ============================================================

with st.container(
    border=True,
    key="chat_shell",
):

    # --------------------------------------------------------
    # MESSAGE AREA
    # --------------------------------------------------------

    with st.container(
        height=470,
        border=False,
        key="chat_history",
    ):

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])


    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    with st.form(
        key="chat_form",
        clear_on_submit=True,
    ):

        input_col, button_col = st.columns(
            [8.4, 1.6],
            gap="small",
        )

        with input_col:

            user_input = st.text_input(
                "Message",
                placeholder="Tell me about your project...",
                label_visibility="collapsed",
            )

        with button_col:

            submitted = st.form_submit_button(
                "Send",
                use_container_width=True,
            )


# ============================================================
# PROCESS MESSAGE
# ============================================================

if submitted and user_input.strip():

    user_message = user_input.strip()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )


    try:

        response = st.session_state.agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id":
                        st.session_state.thread_id
                }
            },
        )

        assistant_response = (
            response["messages"][-1].content
        )

    except Exception as error:

        print("Agent error:", error)

        assistant_response = (
            "I’m having trouble connecting right now. "
            "Please try again in a moment."
        )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )


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