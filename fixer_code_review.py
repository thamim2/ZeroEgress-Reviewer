import streamlit as st
import ollama
from pydantic import BaseModel, Field
from typing import List
from pathlib import Path

# 1. Enhanced Schema to include the Fix
class ReviewItem(BaseModel):
    issue: str = Field(description="The problem found")
    severity: str = Field(description="Low, Medium, or High")
    suggestion: str = Field(description="Explanation of the fix")

class ReviewReport(BaseModel):
    suggestions: List[ReviewItem]
    refactored_code: str = Field(description="The complete, corrected version of the code provided")

# --- UI Setup ---
EXT_TO_LANG = {".py": "Python", ".js": "JavaScript", ".java": "Java", ".cpp": "C++", ".go": "Go"}

st.set_page_config(page_title="AI Code Fixer", layout="wide")
st.title("🛠️ Universal AI Code Fixer")

with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox("Model", ["qwen2.5-coder", "llama3.1"])
    uploaded_file = st.file_uploader("Upload File", type=list(EXT_TO_LANG.keys()))

col1, col2 = st.columns(2)

# Load Content
detected_lang = "JavaScript"
if uploaded_file:
    detected_lang = EXT_TO_LANG.get(Path(uploaded_file.name).suffix, "JavaScript")
    code_content = uploaded_file.getvalue().decode("utf-8")
else:
    with col1:
        detected_lang = st.selectbox("Language", list(EXT_TO_LANG.values()))
        code_content = st.text_area("Paste Code:", height=300)

with col1:
    if code_content:
        st.subheader("Original Code")
        st.code(code_content, language=detected_lang.lower())

# --- Execution ---
if st.button("Fix It For Me"):
    if code_content:
        with st.spinner("Refactoring code locally..."):
            try:
                system_prompt = (
                    f"You are an expert {detected_lang} reviewer, developer and security researcher. "
                    f"Review the following {detected_lang} code for bugs, performance, and best practices. "
                    "For every issue found, provide the EXACT line number and the problematic snippet. "
                    "Then provide the full refactored code."
                )
                
                response = ollama.chat(
                    model=model_name,
                    format=ReviewReport.model_json_schema(),
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': code_content}
                    ],
                    options={'temperature': 0}
                )
                
                report = ReviewReport.model_validate_json(response.message.content)
                
                with col2:
                    st.subheader("Refactored Code")
                    st.code(report.refactored_code, language=detected_lang.lower())
                    
                    st.subheader("Changes Made")
                    for item in report.suggestions:
                        with st.expander(f"[{item.severity}] {item.issue}"):
                            st.write(item.suggestion)
                            
                    # Download Button
                    st.download_button(
                        label="Download Fixed Code",
                        data=report.refactored_code,
                        file_name=f"fixed_{uploaded_file.name if uploaded_file else 'code.txt'}",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"Refactoring failed: {e}")