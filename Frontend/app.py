import streamlit as st
import requests
import json
import os
import uuid
import time

# Set Google-inspired color theme
GOOGLE_COLORS = {
    "black": "#000000",
    "red": "#EA4335",
    "yellow": "#FBBC05",
    "green": "#34A853",
    "background": "#FAF6E9",
    "card": "#DDEB9D",
}

# Set page config with Google colors
st.set_page_config(
    page_title="GreenOps | Cloud Intelligence",
    page_icon="leaf",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Google-inspired CSS
st.markdown(
    f"""
    <style>
    :root {{
        --primary: {GOOGLE_COLORS['black']};
        --background: {GOOGLE_COLORS['background']};
        --card: {GOOGLE_COLORS['card']};
        --assistant-bubble: #E8F0FE;
        --user-bubble: {GOOGLE_COLORS['black']};
    }}
    
    .stApp {{
        background-color: var(--background);
        color: var(--primary);
    }}
    
    .stChatInput {{
        bottom: 20px;
    }}

    .stBottom > div {{
        background: var(--background) !important;
    }}
    
    .stChatInput input {{
        border: 2px solid var(--primary) !important;
        border-radius: 24px !important;
        padding: 12px 20px !important;
    }}
    
    .stChatInput button {{
        background: var(--primary) !important;
        border-radius: 20px !important;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: var(--card) !important;
        border-right: 1px solid #e0e0e0;
        color: black;
    }}
    
    .stChatMessage {{
        padding: 8px 16px;
    }}
    
    [data-testid="stChatMessage-user"] {{
        background-color: var(--user-bubble);
        color: white;
        border-radius: 18px 18px 0 18px;
        margin-left: 25%;
    }}
    
    [data-testid="stChatMessage-assistant"] {{
        background-color: var(--assistant-bubble);
        border-radius: 18px 18px 18px 0;
        margin-right: 25%;
    }}
    
    [data-testid="stBaseButton-secondary"] {{
        background-color: #A0C878;
    }}

    #root > div > div > div > div > section > div > div > div > div > div > div > div > div > div > div > div > p {{
        color: black;
    }}

    [data-testid="stAlertContainer"] {{
        background-color: #F9C0AB;
        color: black;
    }}

    [aria-label="Chat message from assistant"] {{
        color: black;
    }}
    
    .thinking-indicator {{
        display: flex;
        align-items: center;
        color: #5f6368;
        font-style: italic;
        padding: 8px 25px;
    }}
    
    .dot-flashing {{
        position: relative;
        width: 10px;
        height: 10px;
        border-radius: 5px;
        background-color: var(--primary);
        color: var(--primary);
        animation: dotFlashing 1s infinite linear alternate;
        animation-delay: .5s;
        margin-right: 26px;
    }}
    
    .dot-flashing::before, .dot-flashing::after {{
        content: '';
        display: inline-block;
        position: absolute;
        top: 0;
        width: 10px;
        height: 10px;
        border-radius: 5px;
        background-color: var(--primary);
        color: var(--primary);
    }}
    
    .dot-flashing::before {{
        left: -15px;
        animation: dotFlashing 1s infinite alternate;
        animation-delay: 0s;
    }}
    
    .dot-flashing::after {{
        left: 15px;
        animation: dotFlashing 1s infinite alternate;
        animation-delay: 1s;
    }}
    
    @keyframes dotFlashing {{
        0% {{ opacity: 0.6; transform: translateY(2px); }}
        100% {{ opacity: 1; transform: translateY(-2px); }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    :root {
        --greenops-bg: #080b0a;
        --greenops-panel: #101412;
        --greenops-panel-2: #151a17;
        --greenops-border: #29322d;
        --greenops-text: #f4f7f5;
        --greenops-muted: #96a39b;
        --greenops-accent: #87e6b0;
        --greenops-accent-strong: #35b77a;
    }

    html, body, [class*="css"] {
        font-family: Inter, "Segoe UI", Arial, sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 82% 8%, rgba(53, 183, 122, 0.10), transparent 22rem),
            radial-gradient(circle at 12% 90%, rgba(53, 183, 122, 0.05), transparent 24rem),
            var(--greenops-bg) !important;
        color: var(--greenops-text) !important;
    }

    [data-testid="stHeader"] {
        background: transparent;
        backdrop-filter: blur(12px);
    }

    [data-testid="stToolbar"] {
        right: 1rem;
    }

    [data-testid="stSidebar"] {
        background: #0d110f !important;
        border-right: 1px solid var(--greenops-border);
        color: var(--greenops-text) !important;
        min-width: 280px;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.25rem;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #bdc7c1 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: var(--greenops-border);
        opacity: 0.8;
    }

    [data-testid="stSidebar"] button {
        background: var(--greenops-panel-2) !important;
        color: var(--greenops-text) !important;
        border: 1px solid var(--greenops-border) !important;
        border-radius: 10px !important;
        min-height: 42px;
        font-weight: 600;
    }

    [data-testid="stSidebar"] button:hover {
        border-color: var(--greenops-accent-strong) !important;
        background: #19221d !important;
    }

    .block-container {
        max-width: 1060px;
        padding-top: 1.4rem;
        padding-bottom: 7rem;
    }

    .greenops-header {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.25rem 0 1.35rem;
        border-bottom: 1px solid var(--greenops-border);
        margin-bottom: 1.25rem;
    }

    .greenops-brand {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }

    .greenops-mark {
        width: 44px;
        height: 44px;
        display: grid;
        place-items: center;
        border-radius: 12px;
        background: linear-gradient(145deg, #a2edc2, #3bb67b);
        color: #08110d;
        font-size: 23px;
        box-shadow: 0 10px 28px rgba(53, 183, 122, 0.18);
    }

    .greenops-title {
        margin: 0;
        color: var(--greenops-text);
        font-size: 1.45rem;
        line-height: 1.15;
        letter-spacing: -0.02em;
    }

    .greenops-subtitle {
        margin-top: 0.32rem;
        color: var(--greenops-muted);
        font-size: 0.82rem;
    }

    .greenops-live {
        display: inline-flex;
        align-items: center;
        gap: 0.48rem;
        height: 34px;
        padding: 0 11px;
        border: 1px solid var(--greenops-border);
        border-radius: 999px;
        color: #b9c5be;
        background: rgba(16, 20, 18, 0.75);
        font-size: 0.76rem;
        white-space: nowrap;
    }

    .greenops-live-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #56d89a;
        box-shadow: 0 0 10px rgba(86, 216, 154, 0.75);
    }

    .welcome-panel {
        max-width: 720px;
        margin: 2.4rem auto 1.7rem;
        text-align: center;
    }

    .welcome-kicker {
        color: var(--greenops-accent);
        font-size: 0.75rem;
        font-weight: 750;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .welcome-heading {
        margin: 0.6rem 0 0.7rem;
        color: var(--greenops-text);
        font-size: clamp(2rem, 4vw, 3.2rem);
        line-height: 1.02;
        letter-spacing: -0.045em;
    }

    .welcome-copy {
        max-width: 590px;
        margin: 0 auto;
        color: var(--greenops-muted);
        line-height: 1.65;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid var(--greenops-border);
        border-radius: 14px !important;
        padding: 1rem 1.1rem !important;
        margin: 0.55rem 0;
    }

    [data-testid="stChatMessage-user"] {
        background: #151b18 !important;
        color: var(--greenops-text) !important;
        margin-left: 18% !important;
    }

    [data-testid="stChatMessage-assistant"] {
        background: #0f1311 !important;
        margin-right: 18% !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span {
        color: #dbe3de !important;
    }

    [data-testid="stChatMessage"] strong {
        color: var(--greenops-text) !important;
    }

    [data-testid="stChatInput"] {
        max-width: 1060px;
        margin: auto;
        padding: 12px 0 18px;
        background: linear-gradient(180deg, rgba(8, 11, 10, 0), var(--greenops-bg) 32%) !important;
    }

    [data-testid="stChatInput"] textarea {
        background: #111614 !important;
        color: var(--greenops-text) !important;
        border: 1px solid #344038 !important;
        border-radius: 14px !important;
        min-height: 56px;
        padding: 14px 52px 14px 16px;
        caret-color: var(--greenops-accent);
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #78867e !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--greenops-accent-strong) !important;
        box-shadow: 0 0 0 1px rgba(53, 183, 122, 0.22);
    }

    [data-testid="stChatInput"] button {
        background: var(--greenops-accent-strong) !important;
        color: #06100b !important;
        border-radius: 9px !important;
        right: 10px;
    }

    [data-testid="stAlert"] {
        background: #121713 !important;
        border: 1px solid var(--greenops-border) !important;
        color: #bfc9c3 !important;
    }

    .greenops-prompt-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 0 auto 1.2rem;
    }

    .greenops-prompt {
        min-height: 92px;
        padding: 14px;
        border: 1px solid var(--greenops-border);
        border-radius: 12px;
        background: rgba(16, 20, 18, 0.82);
        color: #cbd5cf;
        text-align: left;
    }

    .greenops-prompt strong {
        display: block;
        margin-bottom: 6px;
        color: var(--greenops-text);
        font-size: 0.85rem;
    }

    .greenops-prompt span {
        color: var(--greenops-muted);
        font-size: 0.78rem;
        line-height: 1.45;
    }

    .greenops-footer {
        position: fixed;
        left: 280px;
        right: 0;
        bottom: 0;
        z-index: 20;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(180deg, rgba(8, 11, 10, 0), var(--greenops-bg) 72%);
        color: #68756e;
        font-size: 0.68rem;
        pointer-events: none;
    }

    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            min-width: 240px;
        }

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .greenops-header {
            align-items: center;
        }

        .greenops-live {
            display: none;
        }

        .welcome-panel {
            margin-top: 1.5rem;
        }

        .greenops-prompt-grid {
            grid-template-columns: 1fr;
        }

        [data-testid="stChatMessage-user"] {
            margin-left: 8% !important;
        }

        [data-testid="stChatMessage-assistant"] {
            margin-right: 8% !important;
        }

        .greenops-footer {
            left: 0;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Constants
API_BASE_URL = "https://greenops-agent-service-273345197968.us-central1.run.app"
APP_NAME = "greenops_agent"

# Initialize session state variables
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user-{uuid.uuid4()}"
    
if "session_id" not in st.session_state:
    st.session_state.session_id = None
    
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thinking" not in st.session_state:
    st.session_state.thinking = False

def create_session():
    session_id = f"session-{int(time.time())}"
    response = requests.post(
        f"{API_BASE_URL}/apps/{APP_NAME}/users/{st.session_state.user_id}/sessions/{session_id}",
        headers={"Content-Type": "application/json"},
        data=json.dumps({})
    )
    
    if response.status_code == 200:
        st.session_state.session_id = session_id
        st.session_state.messages = []
        st.rerun()
        return True
    else:
        st.error(f"Failed to create session: {response.text}")
        return False

def send_message(message):
    if not st.session_state.session_id:
        st.error("No active session. Please create a session first.")
        return None

    # Send message to API
    response = requests.post(
        f"{API_BASE_URL}/run",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "app_name": APP_NAME,
            "user_id": st.session_state.user_id,
            "session_id": st.session_state.session_id,
            "new_message": {
                "role": "user",
                "parts": [{"text": message}]
            }
        })
    )

    # st.session_state.thinking = False

    if response.status_code != 200:
        st.error(f"Error: {response.text}")
        return None

    # Process the response
    events = response.json()
    assistant_message = ""
    for item in events:
        parts = item.get("content", {}).get("parts", [])
        for part in parts:
            if not part.get("functionResponse") and part.get("text"):
                assistant_message = part.get("text")

    return assistant_message


# UI Components
st.markdown(
    """
    <div class="greenops-header">
        <div class="greenops-brand">
            <div class="greenops-mark">G</div>
            <div>
                <h1 class="greenops-title">GreenOps</h1>
                <div class="greenops-subtitle">Cloud sustainability intelligence</div>
            </div>
        </div>
        <div class="greenops-live">
            <span class="greenops-live-dot"></span>
            Agent service online
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for session management
with st.sidebar:
    st.markdown(
        """
        <div style="margin-bottom: 0.85rem;">
            <div style="font-size: 0.72rem; color: #78867e; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 700;">Workspace</div>
            <div style="margin-top: 0.35rem; color: #f4f7f5; font-weight: 650;">GreenOps Operations</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("SESSION")
    st.code(st.session_state.session_id or "Not connected", language=None)
    
    if st.session_state.session_id:
        st.success("Session active")
        if st.button("Start new session", use_container_width=True):
            create_session()
    else:
        st.caption("Create a session to begin")
        if st.button("Create session", use_container_width=True, type="primary"):
            create_session()
    
    st.divider()
    st.caption("PLATFORM")
    st.markdown(
        """
        <div style="color: #aebbb4; font-size: 0.82rem; line-height: 1.8;">
            <div>Google Agent Development Kit</div>
            <div>Vertex AI</div>
            <div>BigQuery &amp; Cloud Run</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()
    st.caption(f"User  •  {st.session_state.user_id[:12]}")

# Display chat messages
if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-panel">
            <div class="welcome-kicker">Operational intelligence</div>
            <h2 class="welcome-heading">Make every workload<br>more sustainable.</h2>
            <p class="welcome-copy">
                Analyze infrastructure utilization, forecast emissions, compare machine types,
                and generate executive-ready reports from one workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

if st.session_state.session_id and not st.session_state.messages:
    prompt_columns = st.columns(3)
    prompt_options = [
        ("Optimize infrastructure", "Find underutilized resources and right-sizing opportunities."),
        ("Forecast usage", "Predict CPU, memory, and carbon usage for the next 7 days."),
        ("Generate weekly report", "Summarize regional insights and create a presentation."),
    ]

    for column, (title, description) in zip(prompt_columns, prompt_options):
        with column:
            st.markdown(
                f'<div class="greenops-prompt"><strong>{title}</strong><span>{description}</span></div>',
                unsafe_allow_html=True
            )
            if st.button(title, key=f"prompt_{title}", use_container_width=True):
                st.session_state.pending_message = (
                    "Find infrastructure optimization recommendations"
                    if title == "Optimize infrastructure"
                    else "Forecast CPU, memory, and carbon usage for the next 7 days"
                    if title == "Forecast usage"
                    else "Generate the weekly GreenOps summary report"
                )
                st.session_state.thinking = True
                st.rerun()

for msg in st.session_state.messages:
    avatar = "You" if msg["role"] == "user" else "GO"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Handle user input
if st.session_state.session_id:
    prompt = st.chat_input("Ask about cost savings or carbon reduction...")
    if prompt:
        # Immediately show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Queue message for backend call in next run
        st.session_state.pending_message = prompt
        st.session_state.thinking = True
        st.rerun()
else:
    st.markdown(
        '<div style="text-align:center; color:#78867e; padding:1rem 0;">Create a session from the sidebar to start a conversation.</div>',
        unsafe_allow_html=True
    )

# Step 1: Show thinking animation while message is pending
if "pending_message" in st.session_state and st.session_state.get("thinking", False):
    with st.chat_message("assistant", avatar="🌱"):
        st.markdown(
            '<div class="thinking-indicator">'
            '<div class="dot-flashing"></div>'
            'Working on your request...'
            '</div>',
            unsafe_allow_html=True
        )
    # Set a short delay to render the animation
    time.sleep(1)
    # Now trigger the actual call
    st.session_state.thinking = False  # Let next run do the processing
    st.rerun()

# Step 2: Send message to backend and show response
if "pending_message" in st.session_state and not st.session_state.get("thinking", False):
    user_msg = st.session_state.pending_message
    del st.session_state.pending_message

    assistant_response = send_message(user_msg)
    if assistant_response:
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    st.rerun()


st.markdown(
    """
    <div class="greenops-footer">GreenOps Intelligence Platform  •  Google Cloud Sustainability</div>
    """,
    unsafe_allow_html=True
)