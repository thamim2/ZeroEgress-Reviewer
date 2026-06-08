import streamlit as st
import ollama
import json
from pydantic import BaseModel, Field
from typing import List
from pathlib import Path

# 1. Define the Structured Schema
class ReviewItem(BaseModel):
    issue: str = Field(description="The specific bug or pattern found")
    severity: str = Field(description="Low, Medium, or High")
    suggestion: str = Field(description="How to fix it")

class ReviewReport(BaseModel):
    suggestions: List[ReviewItem]

# 2. Language Mapping Dictionary
EXT_TO_LANG = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
    ".java": "Java", ".cpp": "C++", ".c": "C", ".go": "Go",
    ".rs": "Rust", ".rb": "Ruby", ".php": "PHP", ".html": "HTML"
}

st.set_page_config(page_title="Universal AI Code Reviewer", layout="wide")
st.title("🚀 Universal AI Code Reviewer")

# Sidebar settings
with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox("LLM Model", ["qwen2.5-coder", "llama3.1"])
    uploaded_file = st.file_uploader("Upload a file", type=list(EXT_TO_LANG.keys()))

col1, col2 = st.columns(2)

# Handle language detection
detected_lang = "JavaScript" # Default
if uploaded_file:
    ext = Path(uploaded_file.name).suffix
    detected_lang = EXT_TO_LANG.get(ext, "JavaScript")
    code_content = uploaded_file.getvalue().decode("utf-8")
else:
    with col1:
        detected_lang = st.selectbox("Target Language", list(EXT_TO_LANG.values()))
        code_content = st.text_area("Paste code here:", height=400)

with col1:
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' loaded as {detected_lang}")
        st.code(code_content, language=detected_lang.lower())

with col2:
    if st.button("Analyze Code"):
        if code_content:
            with st.spinner(f"Reviewing {detected_lang} code..."):
                try:
                    response = ollama.chat(
                        model=model_name,
                        format=ReviewReport.model_json_schema(),
                        messages=[
                            {'role': 'system', 'content': f"You are an expert {detected_lang} reviewer."},
                            {'role': 'user', 'content': code_content}
                        ],
                        options={'temperature': 0}
                    )
                    
                    report = ReviewReport.model_validate_json(response.message.content)
                    
                    for item in report.suggestions:
                        with st.expander(f"[{item.severity}] {item.issue}"):
                            st.info(f"💡 {item.suggestion}")
                            
                except Exception as e:
                    st.error(f"Error: {e}")

st.divider()
st.caption("Running locally via Ollama. No data leaves your machine.")