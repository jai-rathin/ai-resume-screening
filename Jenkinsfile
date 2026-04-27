pipeline {
    agent any

    /*
     * CONFIGURATION
     * -------------
     * Set PYTHON_CMD to match your Jenkins agent's Python executable.
     * Windows examples : "python", "py", "C:\\Python312\\python.exe"
     * Linux  examples  : "python3", "/usr/bin/python3"
     *
     * MLFLOW_TRACKING_URI controls where run data is stored.
     * Default 'mlruns' keeps everything local; swap for a remote server URL
     * (e.g. http://mlflow-server:5000) in production.
     */
    environment {
        PYTHON_CMD        = "python"
        MLFLOW_TRACKING_URI = "mlruns"
        VENV_DIR          = "venv"
    }

    stages {

        // ── 1. Checkout ───────────────────────────────────────────────────────
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/jai-rathin/ai-resume-screening.git'
            }
        }

        // ── 2. Setup Virtual Environment & Install Dependencies ───────────────
        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh """
                            ${PYTHON_CMD} -m venv ${VENV_DIR}
                            . ${VENV_DIR}/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        """
                    } else {
                        bat """
                            ${PYTHON_CMD} -m venv ${VENV_DIR}
                            call ${VENV_DIR}\\Scripts\\activate.bat
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        """
                    }
                }
            }
        }

        // ── 3. Lint ───────────────────────────────────────────────────────────
        stage('Lint') {
            steps {
                script {
                    if (isUnix()) {
                        sh """
                            . ${VENV_DIR}/bin/activate
                            pylint app.py train_model.py utils/ \
                                --disable=C0114,C0115,C0116,R0903 \
                                --fail-under=7.0 || true
                        """
                    } else {
                        bat """
                            call ${VENV_DIR}\\Scripts\\activate.bat
                            pylint app.py train_model.py utils/ ^
                                --disable=C0114,C0115,C0116,R0903 ^
                                --fail-under=7.0 || exit /b 0
                        """
                    }
                }
            }
        }

        // ── 4. Train Models (MLflow) ──────────────────────────────────────────
        stage('Train Models') {
            steps {
                script {
                    if (isUnix()) {
                        sh """
                            . ${VENV_DIR}/bin/activate
                            export MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI}
                            ${PYTHON_CMD} train_model.py
                        """
                    } else {
                        bat """
                            call ${VENV_DIR}\\Scripts\\activate.bat
                            set MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI}
                            ${PYTHON_CMD} train_model.py
                        """
                    }
                }
            }
            post {
                success {
                    echo '✅ Both models trained and logged to MLflow.'
                    archiveArtifacts artifacts: 'models/**', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'mlruns/**', allowEmptyArchive: true
                }
                failure {
                    echo '❌ Model training failed. Check MLflow logs above.'
                }
            }
        }

        // ── 5. Test ───────────────────────────────────────────────────────────
        stage('Test') {
            steps {
                script {
                    if (isUnix()) {
                        sh """
                            . ${VENV_DIR}/bin/activate
                            ${PYTHON_CMD} -m pytest test_app.py -v \
                                --tb=short --junit-xml=test-results.xml
                        """
                    } else {
                        bat """
                            call ${VENV_DIR}\\Scripts\\activate.bat
                            ${PYTHON_CMD} -m pytest test_app.py -v ^
                                --tb=short --junit-xml=test-results.xml
                        """
                    }
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        // ── 6. Deploy (start Flask app) ───────────────────────────────────────
        stage('Deploy') {
            steps {
                script {
                    if (isUnix()) {
                        sh """
                            . ${VENV_DIR}/bin/activate
                            nohup ${PYTHON_CMD} app.py &
                            echo "Flask app started in background."
                        """
                    } else {
                        bat """
                            call ${VENV_DIR}\\Scripts\\activate.bat
                            start /B ${PYTHON_CMD} app.py
                            echo Flask app started in background.
                        """
                    }
                }
            }
            post {
                success {
                    echo '🚀 App deployed. Visit http://127.0.0.1:5000'
                    echo '📊 MLflow UI: run  mlflow ui  to explore model runs.'
                }
            }
        }
    }

    // ── Global post-pipeline notifications ───────────────────────────────────
    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Review stage logs above.'
        }
        always {
            echo "Pipeline finished. MLflow experiment: resume-screening"
        }
    }
}
