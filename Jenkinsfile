pipeline {
    agent {
        kubernetes {
            label 'docker-build-agent'
            defaultContainer 'docker'
            yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  containers:
  - name: jenkins-agent
    image: jenkins/inbound-agent:latest
    command:
    - cat
    tty: true
    securityContext:
      privileged: true
  - name: docker
    image: docker:dind
    securityContext:
      privileged: true
  - name: helm
    image: alpine/helm:3.11.1  # Helm container
    command: ['cat']
    tty: true
"""
        }
    }

    environment {
        AWS_CREDENTIALS_ID = 'aws-ecr-credentials'
        ECR_REGISTRY = "864899869895.dkr.ecr.eu-central-1.amazonaws.com"
        ECR_REPO = "tristaprogrammista-bot-x86"
        CONTAINER_NAME = "tristaprogrammista-bot-x86"
        IMAGE_TAG = "latest"
        NAMESPACE = "tristaprogrammista"
        HELM_CHART_NAME = "tristaprogrammista"
        HELM_CHART_DIR = "helm-charts/tristaprogrammista"
        AWS_REGION = "eu-central-1"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Docker') {
            steps {
                script {
                    sh 'dockerd-entrypoint.sh &>/dev/null &'      // Start Docker daemon
                    sh 'sleep 20'                                 // Wait for Docker to initialize
                    sh 'apk add --no-cache aws-cli kubectl curl'  // Install AWS CLI and Kubectl
                    sh 'aws --version'                            // Verify AWS CLI installation
                    sh 'docker --version'                         // Verify Docker installation
                    sh 'kubectl version --client'                 // Verify kubectl installation
                }
            }
        }

        stage('Docker image build') {
            steps {
                script {
                    // Ensure Docker is available in the container and build the image
                    docker.build("${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}")
                    // Optionally, list the Docker images to verify the build
                    sh 'docker images'
                }
            }
        }

        stage('Docker image push to ECR') {
        when { expression { params.PUSH_TO_ECR == true } }
            steps {
                container('docker') {
                    withCredentials([aws(credentialsId: "${AWS_CREDENTIALS_ID}")]) {
                        // Log in to ECR
                        sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login -u AWS --password-stdin ${ECR_REPOSITORY}
                        """
                    }
                    // Push Docker image to ECR
                    sh "docker push ${ECR_REPOSITORY}:${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        success {
            script {
                withCredentials([string(credentialsId: 'TELEGRAM_BOT_TOKEN', variable: 'TELEGRAM_BOT_TOKEN')]) {
                    sh '''
                        curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
                            -d chat_id=20785620 \
                            -d text="Deployment is successful"
                    '''
                }
            }
        }
    }
        failure {
            script {
                sh '''
                    curl -X POST https://api.telegram.org/bot8032258559:AAEDdGjciGE5egx1frzBZFdGViOLq1lPObk/sendMessage \
                    -d chat_id=20785620 \
                    -d text="Deployment is failed"
                '''
            }
        }
    }
}

