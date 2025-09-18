pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t jenkins-cicd-app -f docker/Dockerfile .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 5000:5000 --name jenkins-cicd-app jenkins-cicd-app'
            }
        }
    }

    post {
        always {
            sh 'docker ps -a'
        }
        failure {
            echo 'Build or tests failed!'
        }
    }
}
