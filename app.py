from flask import Flask, render_template, request
from utils.resume_parser import extract_text_from_pdf
from utils.skill_detector import detect_skills
from utils.ats_score import calculate_ats_score
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

# --------------------------------------------------
# UPLOAD FOLDER
# --------------------------------------------------

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")

# Folder automatically create ho jayega
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# --------------------------------------------------
# ALLOWED FILE TYPES
# --------------------------------------------------

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# ANALYZE RESUME
# --------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    # Check file
    if "resume" not in request.files:
        return "<h2>Error: No resume uploaded.</h2>"

    file = request.files["resume"]

    # Check filename
    if file.filename == "":
        return "<h2>Error: No file selected.</h2>"

    # Check PDF
    if not allowed_file(file.filename):
        return "<h2>Error: Only PDF files are allowed.</h2>"

    # Secure filename
    filename = secure_filename(file.filename)

    # Full path
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    # Save uploaded resume
    file.save(file_path)

    try:

        # --------------------------------------------------
        # EXTRACT TEXT
        # --------------------------------------------------

        resume_text = extract_text_from_pdf(file_path)

        # --------------------------------------------------
        # DETECT SKILLS
        # --------------------------------------------------

        skills = detect_skills(resume_text)

        # --------------------------------------------------
        # REQUIRED SKILLS
        # --------------------------------------------------

        required_skills = [
            "python",
            "java",
            "sql",
            "machine learning",
            "git",
            "react",
            "docker",
            "aws"
        ]

        # --------------------------------------------------
        # ATS SCORE
        # --------------------------------------------------

        score, matched_skills, missing_skills = calculate_ats_score(
            skills,
            required_skills
        )

        # --------------------------------------------------
        # RESULT PAGE
        # --------------------------------------------------

        matched_html = "".join(
            f"<li>✓ {skill}</li>"
            for skill in matched_skills
        )

        missing_html = "".join(
            f"<li>✗ {skill}</li>"
            for skill in missing_skills
        )

        detected_html = "".join(
            f"<li>{skill}</li>"
            for skill in skills
        )

        return f"""
        <!DOCTYPE html>

        <html>
        <head>

            <title>Resume Analysis</title>

            <style>

                body {{
                    font-family: Arial, sans-serif;
                    background: #f4f6f8;
                    margin: 0;
                    padding: 40px;
                }}

                .container {{
                    max-width: 900px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }}

                h1 {{
                    text-align: center;
                    color: #222;
                }}

                h2 {{
                    color: #333;
                    margin-top: 30px;
                }}

                .score {{
                    text-align: center;
                    font-size: 40px;
                    font-weight: bold;
                    margin: 20px 0;
                }}

                ul {{
                    line-height: 1.8;
                }}

                .resume-text {{
                    background: #f1f1f1;
                    padding: 20px;
                    border-radius: 8px;
                    white-space: pre-wrap;
                    overflow-x: auto;
                }}

                .back {{
                    display: inline-block;
                    margin-top: 30px;
                    padding: 10px 20px;
                    background: #333;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                }}

            </style>

        </head>

        <body>

            <div class="container">

                <h1>Resume Analysis</h1>

                <div class="score">
                    ATS Score: {score}/100
                </div>


                <h2>Matched Skills</h2>

                <ul>
                    {matched_html}
                </ul>


                <h2>Missing Skills</h2>

                <ul>
                    {missing_html}
                </ul>


                <h2>Detected Skills</h2>

                <ul>
                    {detected_html}
                </ul>


                <h2>Resume Text</h2>

                <div class="resume-text">
                    {resume_text}
                </div>


                <a href="/" class="back">
                    Analyze Another Resume
                </a>

            </div>

        </body>
        </html>
        """

    except Exception as e:

        return f"""
        <h2>Something went wrong while analyzing the resume.</h2>

        <p>
            Error: {str(e)}
        </p>

        <a href="/">Go Back</a>
        """


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )