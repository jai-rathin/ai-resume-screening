pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                git branch: 'main', url: 'https://github.com/jai-rathin/ai-resume-screening.git'
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Setting up Python Virtual Environment...'
                bat '''
                "C:\\Users\\rsacj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m venv venv
                call venv\\Scripts\\activate
                venv\\Scripts\\pip install --upgrade pip
                venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('Run Application') {
            steps {
                echo 'Running Flask App...'
                bat '''
                "C:\\Users\\rsacj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" app.py
                '''
            }
        }

    }

    post {
        always {
            echo 'Pipeline execution complete.'
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please review the logs.'
        }
    }
}