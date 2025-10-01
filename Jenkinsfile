pipeline {
    agent any

    environment {
        APP_NAME       = "jenkins-cicd-app"
        BUILD_NUMBER_INT = env.BUILD_NUMBER.toInteger()  // convert string to integer
        IMAGE_NAME     = "${APP_NAME}:${BUILD_NUMBER}"
        CONTAINER_NAME = "${APP_NAME}-${BUILD_NUMBER}"
        TEST_CONTAINER = "temp-${APP_NAME}-${BUILD_NUMBER}"
        TEST_PORT      = "${5000 + BUILD_NUMBER_INT}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-username/jenkins-cicd-app.git'
            }
        }

        stage('Install dependencies & Run Unit Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t $IMAGE_NAME -f docker/Dockerfile .
                """
            }
        }

        stage('Test Inside Container') {
            steps {
                sh """
                    # Run a temporary container for smoke test
                    docker run --rm -d --name $TEST_CONTAINER -p $TEST_PORT:5000 $IMAGE_NAME
                    sleep 5
                    curl -f http://localhost:$TEST_PORT || (echo "Smoke test failed!" && exit 1)
                """
            }
        }

        stage('Deploy Container') {
            steps {
                sh """
                    # Stop & remove old container if exists
                    if [ "\$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
                        docker stop $CONTAINER_NAME
                    fi
                    if [ "\$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
                        docker rm $CONTAINER_NAME
                    fi

                    # Run new container
                    docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME
                """
            }
        }
    }

    post {
        always {
            // Cleanup unused Docker images
            sh 'docker image prune -f'
            // Optional: archive logs if needed
            archiveArtifacts artifacts: '**/*.log', allowEmptyArchive: true
        }
        success {
            echo "✅ Pipeline complete: New version deployed!"
        }
        failure {
            echo "❌ Build or tests failed!"
        }
    }
}
