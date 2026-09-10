
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
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

ROBOT_PATH = ASSETS_DIR / "robot_hello.json"
LOGO_PATH = ASSETS_DIR / "logo.png"


# ============================================================
# LOAD ROBOT
# ============================================================

def load_robot_animation():
    if not ROBOT_PATH.exists():
        return None

    try:
        with ROBOT_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print("Robot animation error:", error)
        return None


robot_animation = load_robot_animation()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello. I’m the ctrlaltcrew AI Project Consultant. "
                "Tell me about your business or the project you have "
                "in mind, and I’ll guide you through the requirements."
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

logo_html = ""

if LOGO_PATH.exists():
    logo_html = f"""
        <img
            src="file:///{LOGO_PATH.as_posix()}"
            class="brand-logo"
            alt="ctrlaltcrew logo"
        />
    """
else:
    logo_html = """
        <div class="brand-mark">c</div>
    """


st.html(
    f"""
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    html,
    body {{
        background: #06070b !important;
    }}

    .stApp {{
        background:
            radial-gradient(
                900px 600px at 18% 4%,
                rgba(110, 76, 220, 0.14),
                transparent 68%
            ),
            radial-gradient(
                800px 600px at 88% 78%,
                rgba(30, 116, 190, 0.09),
                transparent 65%
            ),
            #06070b;

        color: #f4f5f7;
        min-height: 100vh;
    }}

    .block-container {{
        max-width: 1180px !important;
        padding-top: 0.75rem !important;
        padding-bottom: 3rem !important;
    }}

    /* Remove Streamlit's default spacing around blocks */

    .stElementContainer {{
        margin-bottom: 0 !important;
    }}


    /* ========================================================
       HEADER
       ======================================================== */

    .site-header {{
        height: 68px;
        display: flex;
        align-items: center;
        justify-content: space-between;

        padding: 0 0.2rem;

        border-bottom:
            1px solid rgba(255,255,255,0.06);

        margin-bottom: 3rem;
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: 11px;
    }}

    .brand-logo {{
        width: 31px;
        height: 31px;
        object-fit: contain;
        border-radius: 8px;
    }}

    .brand-mark {{
        width: 31px;
        height: 31px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 9px;

        background:
            linear-gradient(
                135deg,
                #8b5cf6,
                #5b21b6
            );

        color: white;

        font-size: 1.05rem;
        font-weight: 700;
    }}

    .brand-name {{
        font-size: 0.96rem;
        font-weight: 650;
        letter-spacing: -0.015em;
        color: #f2f3f6;
    }}

    .nav {{
        display: flex;
        align-items: center;
        gap: 2rem;
    }}

    .nav-item {{
        color: #868b98;
        text-decoration: none;

        font-size: 0.78rem;

        transition: color 0.2s ease;
    }}

    .nav-item:hover {{
        color: #e7e8ed;
    }}

    .nav-cta {{
        padding: 0.52rem 0.95rem;

        border:
            1px solid rgba(167,139,250,0.25);

        border-radius: 999px;

        color: #ddd7f9;

        background:
            rgba(124,58,237,0.09);
    }}


    /* ========================================================
       HERO
       ======================================================== */

    .hero {{
        text-align: center;
        position: relative;
    }}

    .hero-eyebrow {{
        font-size: 0.68rem;
        font-weight: 650;

        letter-spacing: 0.25em;
        text-transform: uppercase;

        color: #9b82e8;

        margin-bottom: 0.8rem;
    }}

    .hero-title {{
        font-size: clamp(2.35rem, 5vw, 4rem);

        line-height: 1.02;
        letter-spacing: -0.055em;

        font-weight: 730;

        color: #f7f7f9;

        margin: 0;
    }}

    .hero-title span {{
        color: #a78bfa;
    }}

    .hero-subtitle {{
        max-width: 620px;

        margin: 1rem auto 0 auto;

        color: #8b909d;

        font-size: 0.97rem;
        line-height: 1.65;
    }}


    /* ========================================================
       ROBOT
       ======================================================== */

    .robot-stage {{
        position: relative;

        width: 250px;
        height: 190px;

        margin: 0.35rem auto -0.15rem auto;

        display: flex;

        justify-content: center;
        align-items: center;
    }}

    .robot-stage::before {{
        content: "";

        position: absolute;

        width: 150px;
        height: 90px;

        border-radius: 50%;

        background:
            radial-gradient(
                ellipse,
                rgba(117, 87, 230, 0.26),
                rgba(117, 87, 230, 0)
            );

        filter: blur(20px);

        bottom: 25px;
        left: 50%;

        transform: translateX(-50%);
    }}

    .robot-canvas {{
        width: 205px;
        height: 185px;

        position: relative;
        z-index: 1;
    }}


    /* ========================================================
       WELCOME
       ======================================================== */

    .welcome {{
        text-align: center;

        margin-top: 0;
        margin-bottom: 1.35rem;
    }}

    .welcome-title {{
        color: #f2f3f6;

        font-size: 1.13rem;
        font-weight: 620;

        margin-bottom: 0.38rem;
    }}

    .welcome-copy {{
        max-width: 540px;

        margin: 0 auto;

        color: #777d8c;

        font-size: 0.83rem;
        line-height: 1.6;
    }}


    /* ========================================================
       CHAT LABEL
       ======================================================== */

    .chat-shell-label {{
        color: #626875;

        font-size: 0.68rem;
        font-weight: 650;

        letter-spacing: 0.13em;
        text-transform: uppercase;

        margin:
            0 0 0.55rem 0.35rem;
    }}


    /* ========================================================
       MAIN CHAT PANEL
       ======================================================== */

    /* Streamlit bordered container */

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border:
            1px solid rgba(255,255,255,0.075) !important;

        border-radius: 24px !important;

        background:
            rgba(255,255,255,0.025) !important;

        box-shadow:
            0 25px 80px rgba(0,0,0,0.30);

        backdrop-filter: blur(18px);

        padding: 0.8rem !important;
    }}


    /* ========================================================
       SCROLLABLE MESSAGE AREA
       ======================================================== */

    /*
       This targets the fixed-height Streamlit container
       containing the conversation.

       The messages scroll inside this area.
       The input stays below it.
    */

    [data-testid="stVerticalBlockBorderWrapper"]
    [data-testid="stVerticalBlock"] > div {{
        scrollbar-width: thin;
        scrollbar-color:
            rgba(167,139,250,0.25)
            transparent;
    }}


    /* ========================================================
       CHAT MESSAGES
       ======================================================== */

    [data-testid="stChatMessage"] {{
        padding:
            0.72rem 0.8rem;

        border-radius: 18px;

        margin-bottom: 0.55rem;

        border:
            1px solid transparent;
    }}

    [data-testid="stChatMessage"] p {{
        color: #e4e6ec !important;

        font-size: 0.91rem;
        line-height: 1.65;
    }}

    /* User message */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {{
        background:
            rgba(124,58,237,0.095);

        border-color:
            rgba(124,58,237,0.13);
    }}

    /* Assistant message */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {{
        background:
            rgba(255,255,255,0.018);

        border-color:
            rgba(255,255,255,0.045);
    }}

    /* Hide avatars */

    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {{
        display: none !important;
    }}


    /* ========================================================
       MESSAGE ROLE LABELS
       ======================================================== */

    .message-role {{
        font-size: 0.62rem;

        font-weight: 700;

        letter-spacing: 0.12em;

        text-transform: uppercase;

        margin-bottom: 0.22rem;
    }}

    .message-role.ai {{
        color: #a78bfa;
    }}

    .message-role.user {{
        color: #777d8c;
    }}


    /* ========================================================
       CHAT INPUT FORM
       ======================================================== */

    [data-testid="stForm"] {{
        border: none !important;

        padding: 0 !important;

        margin-top: 0.75rem !important;

        background: transparent !important;
    }}

    [data-testid="stForm"] > div {{
        gap: 0 !important;
    }}

    /* Text input */

    [data-testid="stForm"] input {{
        height: 48px !important;

        background:
            rgba(13,14,21,0.96) !important;

        color: #f4f5f7 !important;

        border:
            1px solid rgba(167,139,250,0.22) !important;

        border-radius: 15px !important;

        font-size: 0.90rem !important;

        padding-left: 1rem !important;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.25);
    }}

    [data-testid="stForm"] input:focus {{
        border-color:
            rgba(167,139,250,0.45) !important;

        box-shadow:
            0 0 0 1px rgba(167,139,250,0.12),
            0 12px 35px rgba(0,0,0,0.25) !important;
    }}

    [data-testid="stForm"] input::placeholder {{
        color: #666c79 !important;
    }}


    /* ========================================================
       SEND BUTTON
       ======================================================== */

    [data-testid="stFormSubmitButton"] button {{
        height: 48px !important;

        width: 48px !important;

        min-width: 48px !important;

        margin-left: 0.5rem !important;

        border-radius: 15px !important;

        border:
            1px solid rgba(167,139,250,0.25) !important;

        background:
            rgba(124,58,237,0.14) !important;

        color: #c4b5fd !important;

        font-size: 1.2rem !important;

        transition:
            background 0.2s ease,
            border-color 0.2s ease,
            transform 0.2s ease;
    }}

    [data-testid="stFormSubmitButton"] button:hover {{
        background:
            rgba(124,58,237,0.24) !important;

        border-color:
            rgba(167,139,250,0.42) !important;

        transform: translateY(-1px);
    }}


    /* ========================================================
       SPINNER
       ======================================================== */

    [data-testid="stSpinner"] {{
        color: #a78bfa !important;
    }}


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {{
        text-align: center;

        margin-top: 1.15rem;

        color: #454a55;

        font-size: 0.64rem;

        letter-spacing: 0.05em;
    }}


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 720px) {{

        .block-container {{
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }}

        .site-header {{
            margin-bottom: 2rem;
        }}

        .nav {{
            gap: 0.65rem;
        }}

        .nav-item:not(.nav-cta) {{
            display: none;
        }}

        .hero-title {{
            font-size: 2.25rem;
        }}

        .robot-stage {{
            height: 170px;
        }}

        [data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 20px !important;
        }}
    }}

    </style>


    <!-- =====================================================
         HEADER
         ===================================================== -->

    <div class="site-header">

        <div class="brand">

            {logo_html}

            <div class="brand-name">
                ctrlaltcrew
            </div>

        </div>

        <div class="nav">

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


    <!-- =====================================================
         HERO
         ===================================================== -->

    <div class="hero">

        <div class="hero-eyebrow">
            AI-powered consultation
        </div>

        <h1 class="hero-title">
            AI Project <span>Consultant</span>
        </h1>

        <div class="hero-subtitle">
            Turn your project idea into a clear scope,
            practical recommendation, and next steps.
        </div>

    </div>
    """,
    unsafe_allow_javascript=False,
)


# ============================================================
# ROBOT
# ============================================================

if robot_animation:

    animation_data = json.dumps(robot_animation)

    st.html(
        f"""
        <div class="robot-stage">

            <div
                id="robot-animation"
                class="robot-canvas">
            </div>

        </div>

        <script
            src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js">
        </script>

        <script>

            const robotData = {animation_data};

            lottie.loadAnimation({{
                container:
                    document.getElementById("robot-animation"),

                renderer: "svg",

                loop: true,

                autoplay: true,

                animationData: robotData
            }});

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
                you want to solve. I'll ask the relevant questions
                as we go.
            </div>

        </div>
        """
    )


# ============================================================
# CHAT LABEL
# ============================================================

st.html(
    """
    <div class="chat-shell-label">
        Project consultation
    </div>
    """
)


# ============================================================
# CHAT PANEL
# ============================================================

with st.container(border=True):

    # --------------------------------------------------------
    # SCROLLABLE MESSAGE AREA
    # --------------------------------------------------------

    with st.container(height=450, border=False):

        for message in st.session_state.messages:

            role = message["role"]

            with st.chat_message(role):

                if role == "assistant":

                    st.markdown(
                        '<div class="message-role ai">'
                        'AI CONSULTANT'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                else:

                    st.markdown(
                        '<div class="message-role user">'
                        'YOU'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                st.markdown(message["content"])


    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    with st.form(
        key="project_consultation_form",
        clear_on_submit=True,
        border=False,
    ):

        input_col, button_col = st.columns(
            [1, 0.055],
            gap="small",
        )

        with input_col:

            user_input = st.text_input(
                "Project message",
                placeholder="Tell me about your project...",
                label_visibility="collapsed",
            )

        with button_col:

            submitted = st.form_submit_button(
                "→",
                use_container_width=True,
            )


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if submitted and user_input.strip():

    user_input = user_input.strip()

    # --------------------------------------------------------
    # Save user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )


    # --------------------------------------------------------
    # Generate assistant response
    # --------------------------------------------------------

    try:

        with st.spinner("Thinking..."):

            response = st.session_state.agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input,
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


    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )


    # --------------------------------------------------------
    # Rerun so the new conversation appears in the panel
    # --------------------------------------------------------

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

