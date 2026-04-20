pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/jai-rathin/ai-resume-screening.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"C:\\Users\\rsacj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat '"C:\\Users\\rsacj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pytest'
            }
        }

        stage('Run App') {
            steps {
                bat 'start /B "C:\\Users\\rsacj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" app.py'
            }
        }
    }
}