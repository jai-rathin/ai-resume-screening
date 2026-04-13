pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                bat '"C:\\Users\\rsacj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install --upgrade pip'
                bat '"C:\\Users\\rsacj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Run App') {
            steps {
                bat '"C:\\Users\\rsacj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" app.py'
            }
        }
    }
}