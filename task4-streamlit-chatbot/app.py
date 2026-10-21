"""
Task 4: Interactive Full-Stack AI Chatbot with Streamlit
Reactive conversational interface featuring streaming responses, persona switching,
session isolation, conversation history export, and reset controls.
"""

import os
import sys
import streamlit as st

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from chatbot import ChatbotEngine, ChatMessage

# Streamlit Page Configuration
st.set_page_config(
    page_title="ApexAI — Conversational Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "engine" not in st.session_state:
    st.session_state.engine = ChatbotEngine()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Controls
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    st.markdown("Configure operational parameters and persona system prompts.")

    # Persona Selector
    selected_persona = st.selectbox(
        "Active Persona",
        options=list(ChatbotEngine.PERSONAS.keys()),
        index=0,
        help="Selects specialized system instructions and behavioral heuristics."
    )
    if selected_persona != st.session_state.engine.active_persona:
        st.session_state.engine.set_persona(selected_persona)
        st.toast(f"Switched persona to: {selected_persona}", icon="🎭")

    # Provider Selector
    selected_provider = st.selectbox(
        "Inference Engine",
        options=["Offline Mock Engine (Deterministic)", "Google Gemini 1.5 Flash", "OpenAI GPT-4o-mini"],
        index=0
    )
    prov_key = "mock"
    if "Gemini" in selected_provider:
        prov_key = "gemini"
    elif "OpenAI" in selected_provider:
        prov_key = "openai"
    st.session_state.engine.provider = prov_key

    # Temperature Slider
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

    st.markdown("---")
    st.markdown("### 💾 Session Management")

    # Clear Conversation
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.engine.clear_history()
        st.session_state.messages = []
        st.rerun()

    # Export Transcripts
    if st.session_state.messages:
        json_export = st.session_state.engine.export_history_json()
        st.download_button(
            label="📥 Export JSON",
            data=json_export,
            file_name=f"chat_transcript_{int(st.session_state.engine.history[0].timestamp.replace(':','')) if st.session_state.engine.history else 'export'}.json",
            mime="application/json",
            use_container_width=True
        )

        md_export = st.session_state.engine.export_history_markdown()
        st.download_button(
            label="📄 Export Markdown",
            data=md_export,
            file_name="chat_transcript.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.markdown("---")
    st.caption("ApexAI Suite • Google Antigravity Internship")

# Main Chat Interface Header
st.markdown("## 🤖 ApexAI Conversational Intelligence Hub")
st.caption(f"Currently acting as **{st.session_state.engine.active_persona}** • Provider: **{st.session_state.engine.provider.upper()}**")

# Display Conversation History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "model" in msg and msg["model"]:
            st.caption(f"Model: {msg['model']} • Time: {msg.get('time', '')}")

# Chat Input & Streaming Execution
if prompt := st.chat_input("Ask a question, propose an architecture, or request a code audit..."):
    # 1. Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "time": ChatMessage(role="user", content=prompt).timestamp
    })
    st.session_state.engine.add_user_message(prompt)

    # 2. Assistant Streaming Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        # Stream response tokens
        for chunk in st.session_state.engine.stream_response(prompt):
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)
        st.caption(f"Model: {st.session_state.engine.history[-1].model_used} • Time: {st.session_state.engine.history[-1].timestamp}")

    # Record assistant message in session
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "model": st.session_state.engine.history[-1].model_used,
        "time": st.session_state.engine.history[-1].timestamp
    })
