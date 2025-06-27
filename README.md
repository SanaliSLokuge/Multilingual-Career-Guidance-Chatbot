# 🎓 Multilingual Career Counselor (powered by SUTRA AI)

A simple Streamlit app that uses TWO AI’s **SUTRA** large language model to provide **career advice** in **50+ languages**, with **structured JSON output** and **CV-based personalization**.

---

## 🚀 Features

- 🔤 Multilingual support – Ask questions in your native language  
- 📄 CV upload – Upload your resume as a PDF for personalized feedback  
- 🧠 AI-powered advice – Get career suggestions, skill gaps, relevant courses  
- 📊 Structured JSON output including:
  - 'suggested_career'
  - 'missing_skills'
  - 'relevance_score' (%)
  - 'estimated_time_to_goal'
  - 'recommended_courses'

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/sutra-career-counselor.git
cd sutra-career-counselor
```
2. Install dependencies
Ensure you have Python 3.9+ installed. Then install dependencies with:

```bash
pip install -r requirements.txt
```

Your requirements.txt should include:
streamlit
openai
PyPDF2

3. Set up your SUTRA API key
Create a file named .streamlit/secrets.toml in the root directory and add:

toml
SUTRA_API_KEY = "your_sutra_api_key_here"
🔑 Get your free API key from TWO AI – SUTRA

🧪 Run the app
```bash
streamlit run main.py
```

💡 Example Output
```
{
  "suggested_career": "Data Analyst",
  "missing_skills": ["SQL", "Power BI"],
  "relevance_score": "75%",
  "estimated_time_to_goal": "4 months (full-time learning)",
  "recommended_courses": [
    "Data Analytics with Google",
    "Intro to SQL by Khan Academy"
  ]
}
```
📌 Notes
SUTRA may return extra formatting — fallback displays raw response if needed

PDF parsing accuracy depends on formatting quality (non-scanned works best)

JSON output is ready for dashboards, automation, or further processing

🧠 About SUTRA
SUTRA is a multilingual large language model (LMLM) from TWO AI, supporting 50+ languages with fast inference and structured output capabilities. It’s designed for scalable reasoning, chat, and decision support use cases.


