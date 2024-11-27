pipeline {
    agent {
        kubernetes {
            label 'docker-build-agent'
            defaultContainer 'docker'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    just-a-label: application-deploy
spec:
  containers:
  - name: helm
    image: alpine/helm:3.12.3
    command:
    - cat
    tty: true
  - name: kubectl
    image: bitnami/kubectl:latest
    command:
    - cat
    tty: true
  - name: docker
    image: docker:20.10
    volumeMounts:
    - name: docker-sock
      mountPath: /var/run/docker.sock
    command:
    - /bin/sh
    args:
    - -c
    - "apk add --no-cache curl && cat"
    tty: true
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
"""
        }
    }

    environment {
        ECR_REGISTRY = "https://864899869895.dkr.ecr.eu-central-1.amazonaws.com"
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

        stage('Docker image building and pushing to ECR') {
            steps {
                container('docker') {
                    script {
                        // Inject AWS credentials and authenticate to ECR
                        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-ecr-credentials']]) {
                            // Build the Docker image
                            app = docker.build("${ECR_REPO}:${IMAGE_TAG}")

                            // Push the Docker image to AWS ECR
                            docker.withRegistry("https://${ECR_REGISTRY}", "ecr:${AWS_REGION}:aws-ecr-credentials") {
                                app.push("${env.BUILD_NUMBER}")
                                app.push("latest")
                            }
                        }
                    }
                }
            }
        }

        stage('Deployment to K3s with Helm') {
            steps {
                container('helm') {
                    script {
                        sh """
                        helm upgrade --install ${HELM_CHART_NAME} ${HELM_CHART_DIR}
                        """
                    }
                } 
            }
        }
    }

    post {
        always {
            script {
                sh '''
                    curl -X POST https://api.telegram.org/bot8032258559:AAEDdGjciGE5egx1frzBZFdGViOLq1lPObk/sendMessage \
                    -d chat_id=20785620 \
                    -d text="Always trigger is triggered"
                '''
            }
        }
        success {
            script {
                sh '''
                    curl -X POST https://api.telegram.org/bot8032258559:AAEDdGjciGE5egx1frzBZFdGViOLq1lPObk/sendMessage \
                    -d chat_id=20785620 \
                    -d text="Deployment is successful"
                '''
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