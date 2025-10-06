pipeline {
    agent any

    environment {
        APP_NAME        = "jenkins-cicd-app"
        IMAGE_NAME      = "${APP_NAME}:${BUILD_NUMBER}"
        CONTAINER_NAME  = "${APP_NAME}"
        TEST_CONTAINER  = "temp-${APP_NAME}-${BUILD_NUMBER}"
        TEST_PORT       = 5050   // dedicated temp test port
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
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

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo " Building Docker image..."
                        docker build -t $IMAGE_NAME -f docker/Dockerfile .
        
                        echo " Logging in to Docker Hub..."
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
        
                        echo " Tagging image for Docker Hub..."
                        docker tag $IMAGE_NAME $DOCKER_USER/$APP_NAME:$BUILD_NUMBER
                        docker tag $IMAGE_NAME $DOCKER_USER/$APP_NAME:latest
        
                        echo "Pushing to Docker Hub..."
                        docker push $DOCKER_USER/$APP_NAME:$BUILD_NUMBER
                        docker push $DOCKER_USER/$APP_NAME:latest
                    """
                }
            }
        }

        stage('Smoke Test (Temp Container)') {
            steps {
                sh """
                    echo "Running smoke test on port $TEST_PORT..."
                    docker run --rm -d --name $TEST_CONTAINER -p $TEST_PORT:5000 $IMAGE_NAME
                    sleep 5
                    curl -f http://localhost:$TEST_PORT || (echo "Smoke test failed!" && exit 1)
                    docker stop $TEST_CONTAINER || true
                """
            }
        }

        stage('Deploy Container') {
            steps {
                sh """
                    echo "Deploying $IMAGE_NAME as $CONTAINER_NAME..."

                    # Stop and remove existing container if present
                    if [ "\$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
                        docker stop $CONTAINER_NAME
                    fi
                    if [ "\$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
                        docker rm $CONTAINER_NAME
                    fi

                    # Ensure port 5000 is free
                    fuser -k 5000/tcp || true

                    # Run the latest image
                    docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME
                """
            }
        }
    }

    post {
        always {
            echo " Cleaning up unused images..."
            sh 'docker image prune -f'
            archiveArtifacts artifacts: '**/*.log', allowEmptyArchive: true
        }
        success {
            echo "✅ Pipeline complete: ${APP_NAME} successfully deployed on port 5000!"
        }
        failure {
            echo "❌ Pipeline failed. Check console for details."
        }
    }
}
