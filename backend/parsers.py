import docx
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup


def parse_file(filepath: str) -> str:
    if filepath.endswith(".pdf"):
        text = ""
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    elif filepath.endswith(".docx"):
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    elif filepath.endswith(".txt"):
        return open(filepath, "r").read()
    return ""


def parse_url(url: str) -> str:
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text(" ", strip=True)
