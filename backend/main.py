import os
import shutil
import tempfile

from fastapi import FastAPI, Form, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.agents import run_pipeline
from backend.config import settings
from backend.logging_config import get_access_logger, get_error_logger
from backend.parsers import parse_file, parse_url
from backend.utils import _get_file_extension


error_logger = get_error_logger()
access_logger = get_access_logger()

app = FastAPI(
    title = settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

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
    access_logger.info("Generating Questions")
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


@app.middleware("http")
async def log_requests(request: Request, call_next):
    access_logger.info(f"Incoming request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        access_logger.info(f"Completed with status code: {response.status_code}")
        return response
    except Exception as e:
        error_logger.error(f"Unhandled exception: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
