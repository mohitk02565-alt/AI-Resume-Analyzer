from openai import OpenAI
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


# Get OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")


# Create OpenAI client
client = OpenAI(
    api_key=api_key,
    timeout=60.0,
    max_retries=2
)


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


    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text


    except Exception as e:

        print("========================================")
        print("OPENAI API ERROR")
        print(repr(e))
        print("========================================")

        raise