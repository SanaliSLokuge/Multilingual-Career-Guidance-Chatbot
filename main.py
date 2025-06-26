# main.py
import streamlit as st
from openai import OpenAI

# ✅ Load SUTRA API key securely
api_key = st.secrets["SUTRA_API_KEY"]

# ✅ Initialize Sutra-compatible client
client = OpenAI(
    base_url="https://api.two.ai/v2",
    api_key=api_key
)

# ✅ Page config
st.title("🎓 Multilingual Career Counselor (SUTRA AI)")
st.markdown("Ask any career-related question in your native language and get personalized advice.")

# ✅ Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a multilingual career advisor. "
                "Always reply in the same language as the user. "
                "Provide career advice, suggest learning paths, course options, university suggestions, and affordable alternatives. "
                "Handle follow-up questions like 'Can I do this without a degree?' or 'Where can I study abroad?'."
            )
        }
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of (user_message, assistant_reply)

# ✅ User input for new or first question
user_input = st.text_input("📝 What's your career goal, interest, or question?", key="main_input")

# ✅ Handle initial question
if st.button("Get Advice", key="submit_main"):
    if user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Generating advice..."):
            stream = client.chat.completions.create(
                model="sutra-v2",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=700,
                stream=True
            )

            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    # Optional: real-time update
                    st.markdown(full_response + "▌")

            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.chat_history.append((user_input, full_response))
    else:
        st.warning("Please enter a career question.")

# ✅ Follow-up input
followup_input = st.text_input("💡 Ask a follow-up (e.g., 'Can I do it without a degree?')", key="followup_input")

# ✅ Handle follow-up
if st.button("Ask Follow-Up", key="submit_followup"):
    if followup_input.strip():
        st.session_state.messages.append({"role": "user", "content": followup_input})

        with st.spinner("Following up..."):
            stream = client.chat.completions.create(
                model="sutra-v2",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=700,
                stream=True
            )

            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    # Optional: real-time update
                    st.markdown(full_response + "▌")

            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.chat_history.append((followup_input, full_response))
    else:
        st.warning("Enter a follow-up question.")

# ✅ Display full chat history
st.markdown("---")
st.subheader("📜 Conversation History")
for i, (user_q, bot_a) in enumerate(st.session_state.chat_history):
    st.markdown(f"**You:** {user_q}")
    st.markdown(f"**Sutra:** {bot_a}")
    st.markdown("---")

# ✅ Reset chat option
if st.button("🔁 Reset Conversation"):
    st.session_state.messages = st.session_state.messages[:1]
    st.session_state.chat_history = []
    st.success("Chat history cleared.")
