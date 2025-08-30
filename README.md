# AIG - AI Grill (Agent-powered)

This project generates grilling interview questions based on a **Job Description (JD)** and a **Resume** using **FastAPI**, **Streamlit**, and **Agents (via Agno)** running on a local LLM **Ollama (gemma3:1b)**.

## Features
- Upload JD/Resume (PDF, DOCX, TXT, or URL).
- Agents pipeline:
  1. Extractor → Extracts skills & responsibilities.
  2. Question Generator → Creates grilling interview questions.
- View 10 questions at a time.
- Copy Generated Questions.

## Setup Instructions

### 1. Clone Repo
```bash
git clone https://github.com/jramnai/aig.git
cd aig
```

### 2. Install Requirements
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Setup `.env` file
Copy the `.env.example` file to `.env` and update it
```bash
cp .env.example .env
```

### 4. Install Ollama & Pull Model
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma3:1b
```

### 5. Run Backend (FastAPI)
```bash
uvicorn backend.main:app --reload
```

### 6. Run Frontend (Streamlit)
```bash
# Run this as python module so that it can access backend module
python -m streamlit run frontend/app.py
```

### 7. Run Tests
```bash
pytest
```

## License
MIT

## ✨ Future Enhancements
- Add **Export PDF** (export generated questions as PDF).
- Add **Level of Experience** (level of experience like, junior, mid-level, senior).
- Add **STT support** (speech to text so that user can speak out the answers).
- Add **Feedback Agent** (score candidate answers).
- Add **Session Manager Agent** (track multiple mock interviews).
