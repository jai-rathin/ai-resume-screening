"""
skill_extractor.py
------------------
Extracts technical and soft skills from resume text using NLTK tokenization
and a predefined skill dictionary.
"""

import nltk
from nltk.tokenize import word_tokenize

# ── Download required NLTK data (runs once) ──────────────────────────────────
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

# ── Predefined skill list ────────────────────────────────────────────────────
# Organized by category for easy maintenance.
SKILLS_DB = {
    # Programming Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "ruby",
    "go", "rust", "php", "swift", "kotlin", "scala", "r", "matlab", "perl",
    "dart", "lua", "shell", "bash",

    # Web Development
    "html", "css", "react", "angular", "vue", "node.js", "express",
    "django", "flask", "fastapi", "spring", "bootstrap", "tailwind",
    "jquery", "next.js", "nuxt.js", "svelte",

    # Data & AI / ML
    "machine learning", "deep learning", "nlp", "tensorflow", "pytorch",
    "keras", "pandas", "numpy", "scikit-learn", "opencv", "matplotlib",
    "data analysis", "data science", "artificial intelligence",
    "natural language processing", "computer vision",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "firebase",
    "oracle", "sqlite", "dynamodb", "cassandra",

    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform",
    "ci/cd", "linux", "git", "github", "gitlab",

    # Tools & Misc
    "jira", "figma", "photoshop", "excel", "power bi", "tableau",
    "rest api", "graphql", "microservices", "agile", "scrum",

    # Soft Skills
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "time management", "adaptability", "creativity",
}


def extract_skills(text):
    """
    Extract skills from resume text by tokenizing and matching against
    the predefined skill database.

    Args:
        text (str): Raw text extracted from a resume.

    Returns:
        list: Sorted list of unique skills found in the text.
    """
    if not text:
        return []

    text_lower = text.lower()
    found_skills = set()

    # ── Step 1: Check for multi-word skills (phrases) first ──────────────
    for skill in SKILLS_DB:
        if " " in skill or "." in skill or "/" in skill:
            # Multi-word or special-character skills: search in full text
            if skill in text_lower:
                found_skills.add(skill)

    # ── Step 2: Tokenize and check single-word skills ────────────────────
    try:
        tokens = word_tokenize(text_lower)
    except Exception:
        # Fallback: simple split if tokenizer fails
        tokens = text_lower.split()

    for token in tokens:
        if token in SKILLS_DB:
            found_skills.add(token)

    return sorted(found_skills)
    #testing5
