from typing import List

from agno.agent import Agent
from agno.models.ollama import Ollama

from backend.prompts import (
    EXTRACTOR_INSTRUCTIONS,
    QUESTION_INSTRUCTIONS,
    EXTRACTION_PROMPT_TEMPLATE,
    QUESTION_PROMPT_TEMPLATE,
)


MODEL_ID = "gemma3:1b" 
MODEL = Ollama(id=MODEL_ID)

# Extractor Agent
# Extract key data from JD and Resume
extractor_agent = Agent(
    name="Extractor Agent",
    role="Extracts key skills, responsibilities, and projects from JD and Resume.",
    model=MODEL,
    instructions=EXTRACTOR_INSTRUCTIONS,
)

# Question Generator Agent
# Generate questions based on response of Extractor Agent
question_agent = Agent(
    name="Question Generator Agent",
    role="Generates tough, grilling interview questions based on extracted JD and Resume data.",
    model=MODEL,
    instructions=QUESTION_INSTRUCTIONS,
)


async def run_pipeline(jd_text: str, resume_text: str) -> List[str]:
    """
    Async pipeline:
        1. Extract details from JD + Resume
        2. Generate questions from extracted text
        3. Split/clean into final list
    """
    # 1. Data Extraction
    extraction_prompt = EXTRACTION_PROMPT_TEMPLATE.format(jd_text=jd_text, resume_text=resume_text)
    extraction_resopnse = await extractor_agent.arun(extraction_prompt)
    extracted_content = extraction_resopnse.content

    # 2. Question Generation
    q_gen_prompt = QUESTION_PROMPT_TEMPLATE.format(extracted_content=extracted_content)
    q_gen_response = await question_agent.arun(q_gen_prompt)
    questions_content = q_gen_response.content
    
    # 3. Data Cleaning
    questions = [q.strip(" -1234.\"\n") for q in questions_content.split("\n\n") if q.strip()]
    return questions
