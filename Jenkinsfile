pipeline {
    agent any

    environment {
        IMAGE_NAME = "jenkins-cicd-app"
        CONTAINER_NAME = "jenkins-cicd-app"
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

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $IMAGE_NAME:latest -f docker/Dockerfile .
                '''
            }
        }

        stage('Test Inside Container') {
            steps {
                sh '''
                    # Run container temporarily to validate it starts
                    docker run --rm -d --name temp-$CONTAINER_NAME -p 5000:5000 $IMAGE_NAME:latest
                    sleep 5
                    docker ps | grep temp-$CONTAINER_NAME
                    docker stop temp-$CONTAINER_NAME
                '''
            }
        }

        stage('Deploy Latest') {
            steps {
                sh '''
                    # Stop old container if running
                    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
                        docker stop $CONTAINER_NAME
                    fi
                    if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
                        docker rm $CONTAINER_NAME
                    fi

                    # Run new container
                    docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME:latest
                '''
            }
        }
    }

    post {
        always {
            sh 'docker ps -a'
        }
        failure {
            echo "Build or tests failed!"
        }
        success {
            echo "✅ Pipeline complete: New version deployed!"
        }
    }
}
