pipeline {
    agent {
        kubernetes {
            label 'docker-build-agent'
            defaultContainer 'docker'
        }
    }
    environment {
        ECR_REGISTRY = "864899869895.dkr.ecr.eu-central-1.amazonaws.com"
        ECR_REPO = "tristaprogrammista-bot-x86"
        CONTAINER_NAME = "tristaprogrammista-bot-x86"
        IMAGE_TAG = "latest"
        NAMESPACE = "tristaprogrammista"
        HELM_CHART_DIR = "helm-charts/tristaprogrammista"
        AWS_REGION = "eu-central-1"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh """
                    docker version
                    docker build -t ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG} .
                    docker images  # Verify it was built
                    """
                }
            }
        }

        stage('Run Image Locally') {
            steps {
                script {
                    echo "Running Docker image locally to test..."
                    sh """
                    docker run -d --name ${CONTAINER_NAME} ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}
                    # sleep 5  # Give it a few seconds to start up
                    # curl http://localhost:8080  # Test the service locally (replace with your actual test)
                    docker ps  # Verify it's running
                    """
                }
            }
        }

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
            curl -X POST https://api.telegram.org/bot8032258559:AAEDdGjciGE5egx1frzBZFdGViOLq1lPObk/sendMessage \
            -d chat_id=20785620 \
            -d text="Always"
    }
}