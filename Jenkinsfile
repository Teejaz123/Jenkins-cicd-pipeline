pipeline {
    agent any

    environment {
        APP_NAME       = "jenkins-cicd-app"
        IMAGE_NAME     = "${APP_NAME}:${BUILD_NUMBER}"
        CONTAINER_NAME = "${APP_NAME}-live"
        TEST_CONTAINER = "temp-${APP_NAME}-${BUILD_NUMBER}"
        TEST_PORT      = "$((5000 + BUILD_NUMBER))"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                # Run pytest and generate JUnit XML report
                pytest --maxfail=1 --disable-warnings -q --junitxml=pytest-report.xml
                '''
            }
            post {
                always {
                    // Archive test reports
                    junit 'pytest-report.xml'
                    archiveArtifacts artifacts: 'pytest-report.xml', fingerprint: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Smoke Test in Container') {
            steps {
                sh '''
                docker run -d --name $TEST_CONTAINER -p $TEST_PORT:5000 $IMAGE_NAME
                sleep 5
                curl -f http://localhost:$TEST_PORT || (echo "Smoke test failed!" && exit 1)
                '''
            }
        }

        stage('Cleanup Test Container') {
            steps {
                sh '''
                docker stop $TEST_CONTAINER || true
                docker rm $TEST_CONTAINER || true
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
                docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME
                '''
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f'
            archiveArtifacts artifacts: '**/*.log', allowEmptyArchive: true
        }
        success {
            echo "✅ Pipeline complete: New version deployed successfully!"
        }
        failure {
            echo "❌ Pipeline failed: Check logs and test reports for details."
        }
    }
}
