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
        GITHUB_REPO = "https://github.com/lexxnsk/rsschool-devops-course-task6"
        GITHUB_BRANCH = "main"
        CONTAINER_NAME = "tristaprogrammista-bot-x86"
        IMAGE_TAG = "latest"
        NAMESPACE = "tristaprogrammista"
        HELM_CHART_NAME = "tristaprogrammista"
        HELM_CHART_DIR = "helm-charts/tristaprogrammista"
        AWS_REGION = "eu-central-1"
        WORKSPACE = "./"
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
                }
            }
        }


        // stage('SonarQube check') {
        //     environment {
        //         JAVA_HOME = tool 'JDK'
        //         scannerHome = tool 'SonarQube';
        //     }
        //     steps {
        //         withSonarQubeEnv(credentialsId: 'SonarQube', installationName: 'SonarQube') {
        //             sh """
        //             ${scannerHome}/bin/sonar-scanner \
        //             -Dsonar.sources=$WORKSPACE
        //             """
        //         }
        //     }
        // }

        stage('Prepare Docker container') {
            steps {
                script {
                    sh 'dockerd-entrypoint.sh &>/dev/null &'
                    sh 'sleep 10'
                    sh 'apk add --no-cache aws-cli kubectl curl python'
                    sh 'kubectl version --client'
                    sh 'docker --version'
                    sh 'aws --version'
                    sh 'python --version'
                }
            }
        }


        // stage('Unitaty Tests') {  
        //     steps {
        //         git url: "${GITHUB_REPO}", branch: "${GITHUB_BRANCH}"
        //         container('docker') {
        //             sh "docker build -t word-cloud-generator-builder -f Dockerfile --target builder ."  
        //             sh "docker run --rm word-cloud-generator-builder go test -v ./..." 
        //         }
        //     }
        // }

        stage('Run Python Script') {
            steps {
                script {
                    // Load environment variables from Jenkins
                    env.API_ID = credentials('API_ID')
                    env.API_HASH = credentials('API_HASH')
                    env.PHONE_NUMBER = credentials('PHONE_NUMBER')

                    // Run the Python script with the loaded environment variables
                    sh '''
                        python send.py
                    '''
                }
            }
        }
        
        stage('Docker image build') {
            steps {
                script {
                    docker.build("${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}")
                    sh 'docker images'
                }
            }
        }

        stage('Docker image push to ECR') {
        when { expression { params.PUSH_TO_ECR == true } }
            steps {
                container('docker') {
                    withCredentials([aws(credentialsId: "${AWS_CREDENTIALS_ID}")]) {
                        sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login -u AWS --password-stdin ${ECR_REPOSITORY}
                        """
                    }
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

