import streamlit as st
from typing import Dict, Any, List
from services.ai_service import query_ai_assistant

def render_chatbot(context: Dict[str, Any]):
    """Renders the AI Travel Assistant interactive chat interface."""
    st.markdown("### 🤖 TripGenie AI Travel Assistant")
    st.markdown(
        """
        <p style="color: #94a3b8; font-size: 0.9rem;">
            Ask questions about your destination, weather backups, budget advice, packing lists, or heritage background!
        </p>
        """,
        unsafe_allow_html=True
    )

    if "chat_history" not in st.session_state or st.session_state["chat_history"] is None:
        st.session_state["chat_history"] = []

    # Quick Suggested Prompt Chips
    st.markdown("##### 💡 Suggested Questions")
    chip_cols = st.columns(4)
    quick_prompts = [
        "🎒 What should I pack?",
        "🌧️ Rainy day options?",
        "💰 How to reduce budget?",
        "🏛️ Best heritage site?"
    ]

    selected_quick = None
    for idx, prompt in enumerate(quick_prompts):
        with chip_cols[idx]:
            if st.button(prompt, key=f"quick_prompt_{idx}", use_container_width=True):
                selected_quick = prompt

    # Display Chat History
    for msg in st.session_state["chat_history"]:
        role = msg.get("role")
        content = msg.get("content")
        with st.chat_message(role):
            st.markdown(content)

    # Process prompt
    user_input = st.chat_input("Ask TripGenie AI anything about your trip...")
    active_prompt = user_input or selected_quick

    if active_prompt:
        st.session_state["chat_history"].append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        with st.chat_message("assistant"):
            with st.spinner("TripGenie AI is thinking..."):
                response = query_ai_assistant(
                    user_prompt=active_prompt,
                    context=context,
                    chat_history=st.session_state["chat_history"]
                )
                st.markdown(response)

        st.session_state["chat_history"].append({"role": "assistant", "content": response})
