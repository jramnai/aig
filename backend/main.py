import os
import shutil
import tempfile

from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.agents import run_pipeline
from backend.parsers import parse_file, parse_url
from backend.utils import _get_file_extension


app = FastAPI()

# Enable CORS for Streamlit frontend
# NOTE: Change this for production usage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate-questions")
async def generate_questions_api(
    jd_file: UploadFile | None = None,
    resume_file: UploadFile | None = None,
    jd_url: str | None = Form(None),
    resume_url: str | None = Form(None),
):
    jd_text, resume_text = "", ""

    if jd_file:
        jd_ext = _get_file_extension(jd_file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=jd_ext) as tmp_jd:
            shutil.copyfileobj(jd_file.file, tmp_jd)
            jd_text = parse_file(tmp_jd.name)
            os.unlink(tmp_jd.name)

    if resume_file:
        resume_ext = _get_file_extension(resume_file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=resume_ext) as tmp_resume:
            shutil.copyfileobj(resume_file.file, tmp_resume)
            resume_text = parse_file(tmp_resume.name)
            os.unlink(tmp_resume.name)

    if jd_url:
        jd_text = parse_url(jd_url)
    if resume_url:
        resume_text = parse_url(resume_url)

    if not jd_text or not resume_text:
        return {"error": "Both JD and Resume are required."}

    questions = await run_pipeline(jd_text, resume_text)
    return {"questions": questions}
