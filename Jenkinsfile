pipeline {
    agent {
        kubernetes {
            defaultContainer 'docker'
            yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  containers:
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

    parameters {
        booleanParam(name: 'PUSH_TO_ECR', defaultValue: true, description: 'Should we push the Docker image to ECR?')
    }
    environment {
        AWS_CREDENTIALS_ID = 'aws-ecr-credentials'
        ECR_REGISTRY = "864899869895.dkr.ecr.eu-central-1.amazonaws.com"
        ECR_REPO = "tristaprogrammista-bot-x86"
        IMAGE_TAG = "latest"
        GITHUB_REPO = "https://github.com/lexxnsk/rsschool-devops-course-task6"
        GITHUB_BRANCH = "main"
        K3S_NAMESPACE = "jenkins"
        HELM_CHART_NAME = "tristaprogrammista"
        HELM_CHART_DIR = "helm-charts/tristaprogrammista"
        AWS_REGION = "eu-central-1"
        WORKSPACE = "./"
        JAVA_HOME = '/opt/java/openjdk'  // Make sure this points to your Java installation
        PATH = "${JAVA_HOME}/bin:${PATH}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install curl to the Docker container') {
            steps {
                script {
                    sh 'apk add --no-cache curl'
                    sh 'curl --version'
                    // Install OpenJDK (for example, version 17)
                    sh 'apk add --no-cache openjdk17'
                    // Verify Java installation
                    sh 'java -version'
                }
            }
        }

        stage('SonarQube check') {
            environment {
                scannerHome = tool 'SonarQube';
            }
            steps {
                withSonarQubeEnv(credentialsId: 'SonarQube', installationName: 'SonarQube') {
                    sh """
                    ${scannerHome}/bin/sonar-scanner \
                    -Dsonar.sources=$WORKSPACE
                    """
                }
            }
        }

        stage('Install necessary packets to the Docker container') {
            steps {
                script {
                    sh 'dockerd-entrypoint.sh &>/dev/null &'
                    sh 'sleep 10'
                    sh 'apk add --no-cache aws-cli kubectl curl python3 py3-pip'
                    sh 'kubectl version --client'
                    sh 'docker --version'
                    sh 'aws --version'
                    sh 'python3 --version'
                }
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    docker.build("${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}")
                    sh 'docker images'
                }
            }
        }

        stage('Push Docker image to AWS ECR') {
            steps {
                container('docker') {
                    withCredentials([aws(credentialsId: "${AWS_CREDENTIALS_ID}")]) {
                        sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login -u AWS --password-stdin ${ECR_REGISTRY}
                        """
                    }
                    sh "docker push ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
                }
            }
        }
        
        stage('Deploy Application to K3S using Helm') {
            when { expression { params.PUSH_TO_ECR == true } }
            steps {
                container('helm') {
                    sh """
                    helm upgrade --install ${HELM_CHART_NAME} ./${HELM_CHART_DIR}/ \\
                        --set image.repository=${ECR_REGISTRY}/${ECR_REPO} \\
                        --set image.tag=${IMAGE_TAG} \\
                        --namespace ${K3S_NAMESPACE}
                    """
                }
            }
        }
        
        stage('Verify Application') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'API_ID', variable: 'API_ID'),
                        string(credentialsId: 'API_HASH', variable: 'API_HASH'),
                        string(credentialsId: 'PHONE_NUMBER', variable: 'PHONE_NUMBER'),
                        file(credentialsId: 'SESSION_FILE', variable: 'SESSION_FILE')
                    ]) {
                        sh '''
                            cp "$SESSION_FILE" ./session_name.session
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install -r requirements.txt
                        '''
                        def output = sh(script: 'source venv/bin/activate && python3 send.py && python3 send.py && python3 send.py', returnStdout: true).trim()
                        echo "Output from send.py: ${output}"
                        if (output.contains('otsosi')) {
                            echo "Success: The output contains 'otsosi'."
                        } else {
                            error "Failure: The output does not contain 'otsosi'."
                        }

                    }
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
        failure {
            script {
                withCredentials([string(credentialsId: 'TELEGRAM_BOT_TOKEN', variable: 'TELEGRAM_BOT_TOKEN')]) {
                    sh '''
                        curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
                            -d chat_id=20785620 \
                            -d text="Deployment is failed"
                    '''
                }
            }
        }
    }
}

