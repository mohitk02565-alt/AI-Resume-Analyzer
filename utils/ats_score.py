def calculate_ats_score(resume_text, resume_skills, required_skills):
    """
    Calculate ATS score using:
    Skills       = 40%
    Experience   = 20%
    Education    = 15%
    Projects     = 15%
    Formatting   = 10%
    """

    text = resume_text.lower()

    # -------------------------
    # Skills - 40%
    # -------------------------

    matched_skills = []

    for skill in required_skills:
        if skill.lower() in resume_skills:
            matched_skills.append(skill)

    if required_skills:
        skill_score = (
            len(matched_skills) / len(required_skills)
        ) * 40
    else:
        skill_score = 0

    missing_skills = [
        skill
        for skill in required_skills
        if skill.lower() not in resume_skills
    ]

    # -------------------------
    # Experience - 20%
    # -------------------------

    experience_keywords = [
        "experience",
        "work experience",
        "internship",
        "intern",
        "employment"
    ]

    experience_score = 20 if any(
        keyword in text
        for keyword in experience_keywords
    ) else 0

    # -------------------------
    # Education - 15%
    # -------------------------

    education_keywords = [
        "education",
        "b.tech",
        "btech",
        "bachelor",
        "degree",
        "university",
        "college"
    ]

    education_score = 15 if any(
        keyword in text
        for keyword in education_keywords
    ) else 0

    # -------------------------
    # Projects - 15%
    # -------------------------

    project_keywords = [
        "projects",
        "project",
        "github"
    ]

    project_score = 15 if any(
        keyword in text
        for keyword in project_keywords
    ) else 0

    # -------------------------
    # Formatting - 10%
    # -------------------------

    formatting_sections = [
        "skills",
        "summary",
        "objective",
        "experience",
        "education",
        "projects"
    ]

    sections_found = sum(
        1
        for section in formatting_sections
        if section in text
    )

    formatting_score = (
        sections_found / len(formatting_sections)
    ) * 10

    formatting_score = min(formatting_score, 10)

    # -------------------------
    # Final Score
    # -------------------------

    total_score = (
        skill_score
        + experience_score
        + education_score
        + project_score
        + formatting_score
    )

    score_breakdown = {
        "Skills": round(skill_score),
        "Experience": round(experience_score),
        "Education": round(education_score),
        "Projects": round(project_score),
        "Formatting": round(formatting_score)
    }

    return (
        round(total_score),
        matched_skills,
        missing_skills,
        score_breakdown
    )