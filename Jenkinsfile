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
    - cat
    tty: true
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
      
"""
        }
    }





    environment {
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

        stage('Docker image building and pushing to ECR') {
            steps {
                container('docker') {
                    script {
                        app = docker.build("docker-repo")
                        docker.withRegistry(${ECR_REGISTRY}, ecr:${AWS_REGION}:aws) {
                            app.push("${env.BUILD_NUMBER}")
                            app.push("latest")
                        }
                    }
                }
            }
        }

        stage('Deployment to K3s with Helm') {
            steps {
                container('helm') {
                    script {
                        def releaseName = "wordpress"
                        def chartPath = "./wordpress" 

                        sh """
                        helm upgrade --install ${HELM_CHART_NAME} ${HELM_CHART_DIR}
                        """
                    }
                } 
            }
        }


        // stage('Build Docker Image') {
        //     steps {
        //         script {
        //             echo "Building Docker image..."
        //             sh """
        //             docker version
        //             docker build -t ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG} .
        //             docker images  # Verify it was built
        //             """
        //         }
        //     }
        // }

        // stage('Run Image Locally') {
        //     steps {
        //         script {
        //             echo "Running Docker image locally to test..."
        //             sh """
        //             docker run -d --name ${CONTAINER_NAME} ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}
        //             # sleep 5  # Give it a few seconds to start up
        //             # curl http://localhost:8080  # Test the service locally (replace with your actual test)
        //             docker ps  # Verify it's running
        //             """
        //         }
        //     }
        // }

        // Uncomment the following stages if needed

        // stage('Push to ECR') {
        //     steps {
        //         script {
        //             echo "Pushing Docker image to ECR..."
        //             sh """
        //             aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
        //             docker push ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}
        //             """
        //         }
        //     }
        // }

        // stage('Deploy to K3s with Helm') {
        //     steps {
        //         script {
        //             echo "Deploying to K3s using Helm..."
        //             sh """
        //             helm upgrade --install tristaprogrammista -n ${NAMESPACE} ${HELM_CHART_DIR} --set image.repository=${ECR_REGISTRY}/${ECR_REPO} --set image.tag=${IMAGE_TAG}
        //             """
        //         }
        //     }
        // }

        // stage('Verify Deployment') {
        //     steps {
        //         script {
        //             echo "Verifying the deployment in K3s..."
        //             sh "kubectl get pods -n ${NAMESPACE}"
        //         }
        //     }
        // }
    }

    post {
        always {
            script {
                // Send 'always' notification to Telegram
                sh '''
                    curl -X POST https://api.telegram.org/bot8032258559:AAEDdGjciGE5egx1frzBZFdGViOLq1lPObk/sendMessage \
                    -d chat_id=20785620 \
                    -d text="Always"
                '''
            }
        }
        success {
            script {
                // Send 'always' notification to Telegram
                sh '''
                    curl -X POST https://api.telegram.org/bot8032258559:AAEDdGjciGE5egx1frzBZFdGViOLq1lPObk/sendMessage \
                    -d chat_id=20785620 \
                    -d text="success"
                '''
            }
        }
        failure {
            script {
                // Send 'always' notification to Telegram
                sh '''
                    curl -X POST https://api.telegram.org/bot8032258559:AAEDdGjciGE5egx1frzBZFdGViOLq1lPObk/sendMessage \
                    -d chat_id=20785620 \
                    -d text="failure"
                '''
            }
        }
    }
}

