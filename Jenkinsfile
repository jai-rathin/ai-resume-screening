pipeline {
    agent any

    environment {
        // Defines the Python workspace environment
        PYTHON_ENV = "venv"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Setting up Python Virtual Environment...'
                // Create virtual environment & install dependencies
                bat '''
                    python -m venv %PYTHON_ENV%
                    call %PYTHON_ENV%\\Scripts\\activate.bat
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint / Static Analysis') {
            steps {
                echo 'Running Style Checks...'
                // Basic check to see if the code executes without syntax errors
                bat '''
                    call %PYTHON_ENV%\\Scripts\\activate.bat
                    pylint app.py utils/test_app.py --exit-zero
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running Automated Tests...'
                // Run pytest
                bat '''
                    call %PYTHON_ENV%\\Scripts\\activate.bat
                    pytest test_app.py -v
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment step placeholder...'
                echo 'In a real scenario, this would deploy the app to Heroku/AWS/Azure'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution complete.'
        }
        success {
            echo 'All tests passed successfully! The application is ready.'
        }
        failure {
            echo 'Pipeline failed. Please review the logs.'
        }
    }
}
