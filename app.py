"""
app.py
------
Main Flask application for the AI Resume Screening System.

Routes:
    GET  /       →  Render the main page (upload form + results)
    POST /screen →  Process uploaded PDFs against a job description
"""

import os
from flask import Flask, render_template, request

from utils.pdf_extractor import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.similarity import calculate_similarity

# ── Flask app setup ──────────────────────────────────────────────────────────
app = Flask(__name__)

# Folder where uploaded PDFs are temporarily stored
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Only allow PDF files
ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    """Check if the uploaded file has a .pdf extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Render the main page with the upload form."""
    return render_template("index.html", results=None)


@app.route("/screen", methods=["POST"])
def screen_resumes():
    """
    Process uploaded resumes:
        1. Save each PDF to the uploads folder
        2. Extract text from each PDF
        3. Extract skills from the text
        4. Calculate similarity score vs. the job description
        5. Rank candidates by score (highest first)
        6. Return results to the template
    """

    # Get the job description from the form
    job_description = request.form.get("job_description", "").strip()

    if not job_description:
        return render_template("index.html", results=None,
                               error="Please enter a job description.")

    # Get uploaded files
    files = request.files.getlist("resumes")

    if not files or all(f.filename == "" for f in files):
        return render_template("index.html", results=None,
                               error="Please upload at least one PDF resume.")

    results = []

    for file in files:
        # Skip empty or non-PDF files
        if file.filename == "" or not allowed_file(file.filename):
            continue

        # Save the file
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # ── Pipeline: Extract → Analyze → Score ─────────────────────────
        # Step 1: Extract text from PDF
        resume_text = extract_text_from_pdf(filepath)

        if not resume_text:
            results.append({
                "filename": file.filename,
                "score": 0.0,
                "skills": ["(Could not extract text from this PDF)"],
            })
            continue

        # Step 2: Extract skills
        skills = extract_skills(resume_text)

        # Step 3: Calculate similarity score
        score = calculate_similarity(resume_text, job_description)

        results.append({
            "filename": file.filename,
            "score": score,
            "skills": skills if skills else ["(No skills detected)"],
        })

    # ── Sort results by score (highest first) ────────────────────────────
    results.sort(key=lambda x: x["score"], reverse=True)

    # Add rank numbers
    for i, result in enumerate(results, start=1):
        result["rank"] = i

    return render_template("index.html", results=results,
                           job_description=job_description)


# ── Run the app ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\nResume Screening App is running!")
    print("   Open http://127.0.0.1:5000 in your browser.\n")
    app.run(debug=True)
