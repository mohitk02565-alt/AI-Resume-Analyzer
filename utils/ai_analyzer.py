 
import requests


def analyze_resume_with_ai(resume_text, job_description=""):

    prompt = f"""
You are an expert resume reviewer and career advisor.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Analyze the resume and provide:

1. Resume Summary
2. Strengths
3. Weaknesses
4. Missing Skills
5. Job Match Analysis
6. Specific Improvement Suggestions
7. Overall Recommendation

Keep the response concise, practical, and useful for an internship or entry-level candidate.
"""


    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }
    )


    response.raise_for_status()

    return response.json()["response"]
 
