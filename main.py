# main.py
import streamlit as st
from openai import OpenAI
import PyPDF2
import tempfile

# ✅ Load API Key securely
api_key = st.secrets["SUTRA_API_KEY"]

# ✅ Initialize Sutra-compatible client
client = OpenAI(
    base_url='https://api.two.ai/v2',
    api_key=api_key
)

# ✅ Streamlit UI
st.title("🎓 Multilingual Career Counselor (powered by SUTRA AI)")
st.markdown("Ask your career question in any language, and get relevant course advice instantly.")

# ✅ Upload PDF (CVs, brochures)
doc_text = ""
uploaded_file = st.file_uploader("📄 Upload your CV or related PDF (optional):", type=["pdf"])
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    
    with open(tmp_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        doc_text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)

# ✅ Input prompt
user_input = st.text_area("📝 Enter your career goal or question (in any language):", height=150)

if st.button("Get Career Advice"):
    if not user_input.strip():
        st.warning("Please enter your question first.")
    else:
        with st.spinner("Generating advice..."):
            # ✅ Define system prompt
            system_prompt = {
                "role": "system",
                "content": (
                    "You are a multilingual career advisor. "
                    "Always respond in the same language as the user. "
                    "Provide clear, concise advice and suggest useful online courses or learning paths based on the user's career interest. "
                    "If the user uploaded a CV or PDF, use it to personalize your advice, check if user has the requirements to become the position needed, and suggest what skills are lacking and need to work more on, also mention as a percentage how close the user is to the position and how long it will take the user to achieve the goal if worked full time"
                )
            }

            # ✅ Combine context if document exists
            if doc_text:
                user_message = f"{user_input}\n\nHere is my uploaded document for reference:\n{doc_text[:2000]}"
            else:
                user_message = user_input

            messages = [
                system_prompt,
                {"role": "user", "content": user_message}
            ]

            stream = client.chat.completions.create(
                model="sutra-v2",
                messages=messages,
                temperature=0.7,
                max_tokens=700,
                stream=True
            )

            # ✅ Stream output live
            response_container = st.empty()
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    response_container.markdown(full_response + "▌")

            response_container.markdown(full_response)
