# The RS School - AWS DevOps Course. Project Documentation. Task 7.
---

This repository branch contains a Jenkins Pipeline along with the required configuration adjustments to automate the deployment of Prometheus, an open-source monitoring and alerting system.

## Manual deployment using Helm
The provided code snippet demonstrates how to deploy Prometheus in a Kubernetes cluster using Helm, a package manager for Kubernetes. It involves adding the Bitnami Helm repository, updating the repository index, and using the helm upgrade --install command to deploy the kube-prometheus chart.
- helm repo add bitnami https://charts.bitnami.com/bitnami
- helm repo update
- helm upgrade --install prometheus bitnami/kube-prometheus \
    --set prometheus.service.type=NodePort \
    --set prometheus.service.nodePorts.http=32002 \

## Granting necessary permissions to Jenkins
To ensure the successful execution of the Jenkins pipeline, we need to grant the necessary permissions to Jenkins.
- kubectl apply -f jenkins-role.yaml

## Automated deployment using Jenkins
The Git repository includes a Jenkinsfile that defines a straightforward pipeline. This pipeline is triggered automatically every time changes are pushed to the GitHub repository. A webhook is configured to establish this connection between GitHub and Jenkins, ensuring that the pipeline executes seamlessly with each update.

## Accessing via Internet
An NGINX reverse proxy with SSL certificates is deployed on the Bastion host to ensure secure and encrypted access to the [Prometheus Web UI](https://prometheus.rss.myslivets.ru/). This setup safeguards communication by routing traffic through HTTPS, enhancing security and accessibility.