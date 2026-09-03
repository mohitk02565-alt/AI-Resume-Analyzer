def calculate_ats_score(resume_skills, required_skills):

    if not required_skills:
        return 0, [], []

    matched_skills = []

    for skill in required_skills:
        if skill.lower() in resume_skills:
            matched_skills.append(skill)

    score = (len(matched_skills) / len(required_skills)) * 100

    missing_skills = [
        skill
        for skill in required_skills
        if skill.lower() not in resume_skills
    ]

    return round(score), matched_skills, missing_skills