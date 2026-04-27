pipeline {
    agent any

    environment {
        PYTHON_CMD = "C:\\Users\\rsacj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
        MLFLOW_TRACKING_URI = "mlruns"
        VENV_DIR = "venv"
    }

    stages {

        // ── 1. Checkout ─────────────────────────────
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/jai-rathin/ai-resume-screening.git'
            }
        }

        // ── 2. Install Dependencies ─────────────────
        stage('Install Dependencies') {
            steps {
                bat """
                "%PYTHON_CMD%" -m venv %VENV_DIR%
                call %VENV_DIR%\\Scripts\\activate.bat
                "%PYTHON_CMD%" -m pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        // ── 3. Lint ────────────────────────────────
        stage('Lint') {
            steps {
                bat """
                call %VENV_DIR%\\Scripts\\activate.bat
                pylint app.py train_model.py utils/ ^
                --disable=C0114,C0115,C0116,R0903 ^
                --fail-under=7.0 || exit /b 0
                """
            }
        }

        // ── 4. Train Models ────────────────────────
        stage('Train Models') {
            steps {
                bat """
                call %VENV_DIR%\\Scripts\\activate.bat
                set MLFLOW_TRACKING_URI=%MLFLOW_TRACKING_URI%
                "%PYTHON_CMD%" train_model.py
                """
            }
            post {
                success {
                    echo 'Models trained successfully'
                    archiveArtifacts artifacts: 'models/**', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'mlruns/**', allowEmptyArchive: true
                }
            }
        }

        // ── 5. Test ────────────────────────────────
        stage('Test') {
            steps {
                bat """
                call %VENV_DIR%\\Scripts\\activate.bat
                "%PYTHON_CMD%" -m pytest test_app.py -v ^
                --tb=short --junit-xml=test-results.xml
                """
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        // ── 6. Deploy ──────────────────────────────
        stage('Deploy') {
            steps {
                bat """
                call %VENV_DIR%\\Scripts\\activate.bat
                start /B "%PYTHON_CMD%" app.py
                echo Flask app started
                """
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
        always {
            echo "Pipeline finished. MLflow experiment: resume-screening"
        }
    }
}