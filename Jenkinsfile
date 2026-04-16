pipeline {
    agent any

    stages {

        stage('Setup Environment') {
            steps {
                bat '"C:\\Users\\rsacj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m venv venv'
                bat 'call venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('Run Application') {
            steps {
                bat '"C:\\Users\\rsacj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" app.py'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution complete.'
        }
        failure {
            echo 'Pipeline failed. Please review the logs.'
        }
    }
}