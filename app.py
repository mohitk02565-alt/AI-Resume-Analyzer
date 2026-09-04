from flask import Flask, render_template, request
from utils.resume_parser import extract_text_from_pdf
from utils.skill_detector import detect_skills
from utils.ats_score import calculate_ats_score
from utils.ai_analyzer import analyze_resume_with_ai
from werkzeug.utils import secure_filename

import os
import re


app = Flask(__name__)


# ==========================================
# Upload Configuration
# ==========================================

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = {"pdf"}


# ==========================================
# Skills Database
# ==========================================

REQUIRED_SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",
    "mysql",
    "mongodb",
    "flask",
    "django",
    "react",
    "node.js",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "power bi",
    "excel",
    "docker",
    "aws"
]


# ==========================================
# File Validation
# ==========================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================================
# Job Description Matching
# ==========================================

def calculate_job_match(
    resume_skills,
    job_description
):

    if not job_description.strip():

        return 0, [], []

    jd_text = job_description.lower()

    jd_skills = []

    for skill in REQUIRED_SKILLS:

        if skill.lower() in jd_text:

            jd_skills.append(skill)

    if not jd_skills:

        return 0, [], []

    matched = [
        skill
        for skill in jd_skills
        if skill.lower() in resume_skills
    ]

    missing = [
        skill
        for skill in jd_skills
        if skill.lower() not in resume_skills
    ]

    score = round(
        (len(matched) / len(jd_skills)) * 100
    )

    return score, matched, missing


# ==========================================
# Resume Suggestions
# ==========================================

def generate_suggestions(
    resume_text,
    skills,
    missing_skills,
    job_description=""
):

    suggestions = []

    text = resume_text.lower()

    # --------------------------------------
    # Resume Sections
    # --------------------------------------

    sections = {

        "Experience": [
            "experience",
            "work experience",
            "employment"
        ],

        "Education": [
            "education",
            "qualification",
            "degree"
        ],

        "Projects": [
            "projects",
            "project"
        ],

        "Skills": [
            "skills",
            "technical skills"
        ]
    }

    for section, keywords in sections.items():

        if not any(
            keyword in text
            for keyword in keywords
        ):

            suggestions.append(
                f"Add a clear {section} section."
            )

    # --------------------------------------
    # Skills
    # --------------------------------------

    if len(skills) < 5:

        suggestions.append(
            "Add more relevant technical skills "
            "that match your target role."
        )

    # --------------------------------------
    # Projects
    # --------------------------------------

    if "project" not in text:

        suggestions.append(
            "Add 2-3 relevant projects with "
            "technologies and measurable results."
        )

    # --------------------------------------
    # Numbers / Achievements
    # --------------------------------------

    if not re.search(
        r"\b\d+%|\b\d+\+|\b\d+\b",
        resume_text
    ):

        suggestions.append(
            "Add measurable achievements using "
            "numbers, percentages, or metrics."
        )

    # --------------------------------------
    # Job Description
    # --------------------------------------

    if (
        job_description.strip()
        and missing_skills
    ):

        suggestions.append(
            "Consider adding relevant missing skills "
            "if you genuinely have experience with them."
        )

    return suggestions[:6]


# ==========================================
# Home Page
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# Resume Analysis
# ==========================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    # --------------------------------------
    # Check File
    # --------------------------------------

    if "resume" not in request.files:

        return (
            "<h2>Error: No resume uploaded.</h2>"
        )

    file = request.files["resume"]

    if file.filename == "":

        return (
            "<h2>Error: No file selected.</h2>"
        )

    if not allowed_file(file.filename):

        return (
            "<h2>Error: Only PDF files are allowed.</h2>"
        )

    # --------------------------------------
    # Save File
    # --------------------------------------

    filename = secure_filename(
        file.filename
    )

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(file_path)

    try:

        # ==================================
        # 1. Extract Resume Text
        # ==================================

        resume_text = extract_text_from_pdf(
            file_path
        )

        # ==================================
        # 2. Detect Skills
        # ==================================

        skills = detect_skills(
            resume_text
        )

        # ==================================
        # 3. ATS Score
        # ==================================

        (
            ats_score,
            matched_skills,
            missing_skills,
            score_breakdown
        ) = calculate_ats_score(
            resume_text,
            skills,
            REQUIRED_SKILLS
        )

        # ==================================
        # 4. Job Description
        # ==================================

        job_description = request.form.get(
            "job_description",
            ""
        )

        # ==================================
        # 5. Job Match
        # ==================================

        (
            job_match,
            job_matched,
            job_missing
        ) = calculate_job_match(
            skills,
            job_description
        )

        # ==================================
        # 6. Suggestions
        # ==================================

        suggestions = generate_suggestions(
            resume_text,
            skills,
            missing_skills,
            job_description
        )


        # ==================================
        # 7. AI Analysis
        # ==================================

        ai_analysis = analyze_resume_with_ai(
            resume_text,
            job_description
        )

        # ==================================
        # 7. Render Dashboard
        # ==================================

        return render_template(
            "index.html",

            analyzed=True,

            ats_score=ats_score,

            job_match=job_match,

            skills=skills,

            matched_skills=matched_skills,

            missing_skills=missing_skills,

            job_matched=job_matched,

            job_missing=job_missing,

            suggestions=suggestions,
            ai_analysis=ai_analysis,

            score_breakdown=score_breakdown,

            resume_text=resume_text
        )

    except Exception as e:

        return f"""
        <h2>
            Something went wrong while
            analyzing the resume.
        </h2>

        <p>
            Error: {str(e)}
        </p>

        <a href="/">
            Go Back
        </a>
        """


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )