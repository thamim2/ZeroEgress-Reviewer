import streamlit as st
import ollama
import json
from pydantic import BaseModel, Field
from typing import List

# 1. Define the Schema
class ReviewItem(BaseModel):
    issue: str = Field(description="The specific problem identified in the code")
    severity: str = Field(description="Low, Medium, or High")
    suggestion: str = Field(description="The recommended fix or improvement")

class ReviewReport(BaseModel):
    suggestions: List[ReviewItem]

# Page Config
st.set_page_config(page_title="JS Code Reviewer Pro", layout="wide")
st.title("🛡️ Structured JS Reviewer")

col1, col2 = st.columns(2)

with col1:
    code_input = st.text_area("Paste JS Code:", height=400)
    model_name = st.selectbox("Model", ["qwen2.5-coder", "llama3.1", "mistral"])

with col2:
    if st.button("Analyze Code"):
        if code_input:
            with st.spinner("Analyzing..."):
                try:
                    # 2. Call Ollama with the Pydantic Schema
                    response = ollama.chat(
                        model=model_name,
                        # This line is the magic! It forces the model to follow your class.
                        format=ReviewReport.model_json_schema(), 
                        messages=[
                            {'role': 'system', 'content': "You are a JavaScript code reviewer. Provide structured feedback."},
                            {'role': 'user', 'content': code_input}
                        ],
                        options={'temperature': 0} # Set to 0 for strict consistency
                    )

                    # 3. Extract and Parse
                    raw_content = response.message.content
                    
                    # DEBUG: Show what the model actually sent
                    with st.expander("Show Raw Debug Info"):
                        st.text(raw_content)

                    # Validate the JSON against our Pydantic model
                    report = ReviewReport.model_validate_json(raw_content)

                    # 4. Display reliably
                    for item in report.suggestions:
                        with st.expander(f"[{item.severity}] {item.issue}"):
                            st.info(f"💡 {item.suggestion}")

                except Exception as e:
                    st.error(f"Analysis failed: {e}")