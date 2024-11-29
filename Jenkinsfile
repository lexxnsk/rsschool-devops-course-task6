pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  containers:
  - name: helm
    image: alpine/helm:3.11.1
    command: ['cat']
    tty: true
"""
        }
    }

    environment {
        PROMETHEUS_PORT = "32002"
        K3S_NAMESPACE = "jenkins"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy Application to K3S using Helm') {
            steps {
                container('helm') {
                    sh """
                    helm repo add bitnami https://charts.bitnami.com/bitnami
                    helm repo update
                    helm upgrade --install prometheus bitnami/kube-prometheus \\
                    --set prometheus.service.type=NodePort \\
                    --set prometheus.service.nodePorts.http=${PROMETHEUS_PORT} \\
                    --namespace ${K3S_NAMESPACE}
                    """
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

