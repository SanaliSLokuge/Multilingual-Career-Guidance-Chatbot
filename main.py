# main.py
import streamlit as st
from openai import OpenAI
import PyPDF2
import tempfile
import json

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
        with st.spinner("Generating structured advice..."):
            # ✅ Define system prompt for structured output
            system_prompt = {
                "role": "system",
                "content": (
                    "You are a multilingual career advisor. "
                    "Always respond in the same language as the user. "
                    "Return your reply strictly as a JSON object with the following keys: "
                    "suggested_career, missing_skills (list), relevance_score (percentage as string), estimated_time_to_goal (as string), recommended_courses (list of course names). "
                    "If the user uploaded a CV or PDF, use it to personalize your advice."
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

            # ✅ Get full output (non-streaming for JSON parsing)
            try:
                response = client.chat.completions.create(
                    model="sutra-v2",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=700
                )
                content = response.choices[0].message.content

                parsed = json.loads(content)
                st.success("🌐 Structured Career Advice")
                st.json(parsed)

            except json.JSONDecodeError:
                st.error("Failed to parse structured response. Showing raw output below:")
                st.markdown(content)
            except Exception as e:
                st.error(f"API error: {e}")
