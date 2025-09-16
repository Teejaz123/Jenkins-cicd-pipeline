pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t jenkins-cicd-app ./docker'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest app/tests/'
            }
        }

        stage('Run') {
            steps {
                sh 'docker run -d -p 5000:5000 --name cicd-app jenkins-cicd-app'
            }
        }
    }

    post {
        always {
            sh 'docker ps -a'
        }
    }
}
