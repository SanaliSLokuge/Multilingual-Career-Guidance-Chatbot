import streamlit as st
from openai import OpenAI

# ✅ Load API Key securely
api_key = st.secrets["SUTRA_API_KEY"]

# ✅ Initialize Sutra-compatible OpenAI client
client = OpenAI(
    base_url="https://api.two.ai/v2",
    api_key=api_key
)

# ✅ UI
st.title("🎓 Multilingual Career Counselor (SUTRA AI)")
st.markdown("Ask any career-related question in your native language and get personalized advice.")

# ✅ Init session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": (
            "You are a multilingual career advisor. "
            "Always reply in the same language as the user. "
            "Provide advice, online course suggestions, career planning tips, and handle follow-ups like 'Is that possible without a degree?' or 'Suggest something cheaper'."
        )
    }]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ Primary input
user_input = st.text_input("📝 What's your career goal, interest, or question?", key="main_input")

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
                    full_response += chunk.choices[0].delta.content

            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("SUTRA", full_response))
    else:
        st.warning("Please enter a career question.")

# ✅ Follow-up input
st.markdown("💬 *You can ask follow-up questions after getting a response.*")
followup_input = st.text_input("💡 Ask a follow-up (e.g., 'Can I do it without a degree?')", key="followup_input")

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
                    full_response += chunk.choices[0].delta.content

            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.chat_history.append(("You", followup_input))
            st.session_state.chat_history.append(("SUTRA", full_response))
    else:
        st.warning("Enter a follow-up question.")

# ✅ Display full chat history
st.markdown("---")
st.subheader("📜 Conversation History")
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 {role}:** {msg}")
    else:
        st.markdown(f"**🤖 {role}:** {msg}")
    st.markdown("---")

# ✅ Reset
if st.button("🔄 Reset Conversation"):
    st.session_state.messages = st.session_state.messages[:1]
    st.session_state.chat_history = []
    st.success("Conversation history cleared.")
