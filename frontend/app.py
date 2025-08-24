import requests
import streamlit as st

from backend.config import settings


API_URL = "http://localhost:8000/generate-questions"

st.set_page_config(page_title=settings.PROJECT_NAME, layout="wide")

st.title(settings.PROJECT_NAME)
st.write("Upload JD and Resume to generate grilling interview questions.")

jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"])
resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
jd_url = st.text_input("Or enter JD URL")
resume_url = st.text_input("Or enter Resume URL")

if st.button("Generate Questions"):
    with st.spinner("Generating questions..."):
        files, data = {}, {}
        if jd_file:
            files["jd_file"] = jd_file
        if resume_file:
            files["resume_file"] = resume_file
        if jd_url:
            data["jd_url"] = jd_url
        if resume_url:
            data["resume_url"] = resume_url

        res = requests.post(API_URL, files=files, data=data)
        if res.status_code == 200:
            response = res.json()
            if "error" in response:
                st.error(response["error"])
            else:
                st.session_state.questions = response["questions"]
        else:
            st.error("API Error")

if "questions" in st.session_state:
    questions = st.session_state.questions
    page = st.number_input("Page", min_value=1, max_value=(len(questions) // 10 + 1))
    start, end = (page - 1) * 10, page * 10
    st.write("### Interview Questions")
    for i, q in enumerate(questions[start:end], start=start + 1):
        st.write(f"**Q{i}:** {q}")

    if st.button("Copy to Clipboard"):
        st.code("\n".join(questions[start:end]))
