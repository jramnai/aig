EXTRACTOR_INSTRUCTIONS = (
    "Extract the candidate-relevant skills, frameworks, domains, seniority, "
    "notable projects and responsibilities from the JD and the resume. "
    "Return a concise bullet list only; no intro/outro."
)

QUESTION_INSTRUCTIONS = (
    "Generate 15–20 rigorous interview questions tailored to the JD and candidate profile. "
    "Focus on architecture decisions, trade-offs, debugging, scalability, data handling, APIs, tests. "
    "Output ONLY the questions (one per line). Do NOT add any preamble like 'Here are...'. "
    "Avoid numbering and quotes."
)

EXTRACTION_PROMPT_TEMPLATE = """
You are an expert JD & resume analyzer.
Extract key skills, good to have skills, preferred skills, must to have skills, required level of experience, role and responsibilities from the following provided JD text.
{jd_text}
Extract key skills, projects, and experiences from the following provided resume text.
{resume_text}
Return a compact list of skill tags, tech, frameworks, domains, seniority and noteworthy projects.
"""

QUESTION_PROMPT_TEMPLATE = """
You are an interview question generator.
Using this extracted context:
{extracted_content}
Write 20 rigorous interview questions for THIS job. Only output the questions (one per line).
Generate 20 tailored interview questions for this job.
Focus on:
- Technical depth
- Project experience
- Problem-solving
- System design
- Out of the box thinking
- Open source contributions if any
- Certifications if any
Strictly follow following instructions:
- Do not include numbering, explanations, or extra text.
- Only output the questions (one per line).
- Use \n\n as question separator.
- Do not include intro/outro text.

Following is example output format:
what is your python experience?\n\nDisucss about your current project\n\nPlease speak about your strength and weakness
"""
