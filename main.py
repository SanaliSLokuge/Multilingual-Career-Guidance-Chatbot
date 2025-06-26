# main.py
import streamlit as st
from openai import OpenAI

# ✅ Load API Key securely (from .streamlit/secrets.toml)
api_key = st.secrets["SUTRA_API_KEY"]

# ✅ Initialize Sutra-compatible client
client = OpenAI(
    base_url='https://api.two.ai/v2',
    api_key=api_key
)

# ✅ Streamlit UI
st.title("🎓 Multilingual Career Counselor (powered by SUTRA AI)")
st.markdown("Ask your career question in any language, and get relevant course advice instantly.")

user_input = st.text_area("📝 Enter your career goal or question (in any language):", height=150)

if st.button("Get Career Advice"):
    if not user_input.strip():
        st.warning("Please enter your question first.")
    else:
        with st.spinner("Generating advice..."):
            # Define system prompt
            system_prompt = {
                "role": "system",
                "content": (
                    "You are a multilingual career advisor. "
                    "Always respond in the same language as the user. "
                    "Provide clear, concise advice and suggest useful online courses or learning paths based on the user's career interest."
                )
            }

            messages = [
                system_prompt,
                {"role": "user", "content": user_input}
            ]

            stream = client.chat.completions.create(
                model="sutra-v2",
                messages=messages,
                temperature=0.7,
                max_tokens=600,
                stream=True
            )

            # Stream output live
            response_container = st.empty()
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    response_container.markdown(full_response + "▌")

            response_container.markdown(full_response)
