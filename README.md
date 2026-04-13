# AI Resume Screener (CI/CD Ready)

A Flask-based Artificial Intelligence Resume Screener that uses Natural Language Processing (NLP) to extract skills from resumes and compare them to a given job description using Cosine Similarity. 

This project goes a step further by being **Continuous Integration/Continuous Deployment (CI/CD) ready**.

## GitHub Project Structure

```text
.
├── .gitignore               # Ensures temporary files don't pollute the repository
├── Jenkinsfile              # Jenkins Pipeline definition for CI/CD
├── README.md                # Documentation (You are here)
├── app.py                   # Main Flask application
├── requirements.txt         # All Python package dependencies
├── test_app.py              # Automated Unit Tests for the pipeline
├── static/                  # CSS styles
│   └── style.css
├── templates/               # HTML Views
│   └── index.html
└── utils/                   # Modular Python helpers
    ├── __init__.py
    ├── pdf_extractor.py
    ├── similarity.py
    └── skill_extractor.py
```

## How to Run Locally

1. Create a virtual environment:
   ```bash
   python -m venv venv
   # Activate it (Windows)
   venv\Scripts\activate
   # Activate it (Mac/Linux)
   source venv/bin/activate
   ```
2. Install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the web interface at `http://127.0.0.1:5000`

---

## CI/CD Instructions (Jenkins Setup)

This project contains a `Jenkinsfile` configuring a standardized Continuous Integration pipeline. It demonstrates three core DevOps practices:
1. **Build Environment Setup**: Installs dependencies in an isolated space.
2. **Static Analysis & Linting**: Checks code quality.
3. **Automated Testing**: Validates application routes.

### Steps to demo with Jenkins:

1. **Push to GitHub**:
   Push this entire folder to a repository on your GitHub account. Do not upload the `venv` or `uploads` folders (the `.gitignore` handles this automatically).

2. **Connect Jenkins**:
   - Install Jenkins on your machine or server.
   - Go to Jenkins Dashboard > **New Item**.
   - Enter a name (e.g., `resume-screener-pipeline`).
   - Select **Pipeline** and click OK.

3. **Configure the Pipeline**:
   - Scroll down to the **Pipeline** section.
   - Change "Definition" to **Pipeline script from SCM**.
   - Select **Git** as the SCM.
   - Paste your GitHub repository URL into the "Repository URL" field.
   - Under "Script Path", ensure it says `Jenkinsfile`.
   - Click Save.

4. **Build Now**:
   - Click **Build Now** on the left menu.
   - You will see stages executing: `Checkout` -> `Setup Environment` -> `Lint` -> `Test` -> `Deploy`.
   - Check the **Console Output** for any stage to see Jenkins installing your `requirements.txt` and passing the internal tests from `test_app.py`.
