pipeline {
    agent {
        node {
            label 'Prod-Node' // Aapke Slave node ka label
        }
    }

    environment {
        DOCKER_HUB_CRED_ID = 'dockerhub-creds'
        DOCKER_USER        = 'momin091'
        IMAGE_NAME         = 'stats-app'
        IMAGE_TAG          = "${BUILD_NUMBER}"
    }

    stages {
        stage('Code Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                    pytest test_app.py -v
                '''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: "${DOCKER_HUB_CRED_ID}", 
                        passwordVariable: 'DOCKER_PASS', 
                        usernameVariable: 'DOCKER_USER_ENV'
                    )]) {
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER_ENV" --password-stdin
                            
                            docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} \
                                         -t ${DOCKER_USER}/${IMAGE_NAME}:latest .
                            
                            docker push ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                            docker push ${DOCKER_USER}/${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy Container Locally on Slave') {
            steps {
                sh '''
                    # Old container stop karke naya image run karna
                    docker stop stats-app || true
                    docker rm stats-app || true
                    
                    docker run -d \
                      --name zeno-production-app \
                      --restart always \
                      -p 80:5000 \
                      -e APP_VERSION=${IMAGE_TAG} \
                      ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                    
                    docker image prune -f
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    python3 scripts/health_check.py --url http://localhost/api/status
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo "CI/CD Pipeline Successful! App is running on Slave Node Port 80."
        }
        failure {
            echo "Pipeline failed. Check stage logs."
        }
    }
}
