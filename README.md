# Offline Code Review & Refactoring Suite 🚀

A progressive suite of local, privacy-first AI development tools built with Streamlit, Pydantic, and Ollama. This repository demonstrates an architectural progression from a single-language diagnostic prototype to an automated, multi-language code refactoring engine—all running fully offline without external API dependencies.

## 🛠️ Suite Directory

The repository is broken down into three logical evolutionary steps:

### 1. JavaScript Prototyper (`js_code_reviewer.py`)
* **Objective:** Establish reliable structured JSON generation.
* **Features:** Enforces strict compliance to Pydantic definitions (`ReviewReport`) using Ollama's schema features to prevent model output fracturing. Includes raw debug views for API inspection.

### 2. Universal Polyglot Scanner (`all_lang_code_review.py`)
* **Objective:** Abstract structure generation to support multiple codebases.
* **Features:** Automatically detects target languages via uploaded file extensions (`.py`, `.js`, `.ts`, `.java`, `.cpp`, `.go`, `.rs`, `.rb`, `.php`, `.html`). Dynamically alters system constraints based on the detected language runtime.

### 3. Automated Refactoring Engine (`fixer_code_review.py`)
* **Objective:** Transition from passive analysis to active code modification.
* **Features:** Enlarges JSON boundaries to pull down the fully modified code string. Presents side-by-side comparative UI columns (`Original` vs `Refactored`), provides itemized explanations for changes, and provides browser-native source code downloads (`fixed_code.txt`).

---

## 🧠 Core System Architecture

* **Structured JSON Extraction:** Every module leverages Pydantic models passed through `ollama.chat(format=Model.model_json_schema())` combined with a strict `temperature=0` configuration to ensure runtime determinism.
* **Data Security & Privacy:** Zero-egress architecture. Source code analysis remains local to your host engine.

---

## ▶ Running the Suite Locally

### 1. System Prerequisites
Download and launch [Ollama](https://ollama.com/). Pull down your preferred coding and inference models:
```bash
ollama pull qwen2.5-coder
ollama pull llama3.1

### 2. Dependencies Setup
pip install streamlit ollama pydantic

### 3. Execution

# To run the initial prototype:
streamlit run js_code_reviewer.py

# To run the multi-language scanner:
streamlit run all_lang_code_review.py

# To run the complete automated refactoring engine:
streamlit run fixer_code_review.py


