# The RS School - AWS DevOps Course. Project Documentation. Task 9.
---

This repository branch contains a Jenkins Pipeline along with the required configuration adjustments to automate the deployment of Alerting in Grafana, a multi-platform open source analytics and interactive visualization web application.

## Manual deployment using Helm
The provided code snippet demonstrates how to deploy Grafana with a proper SMTP configuration in a Kubernetes cluster using Helm, a package manager for Kubernetes. It involves adding the Bitnami Helm repository, updating the repository index, and using the helm upgrade --install command to deploy the grafana chart.
```
helm upgrade --install grafana bitnami/grafana \
--set service.type=NodePort \
--set service.nodePorts.grafana=32003 \
--set admin.password=<xxxxxxxxxxxxxxxxxxx> \
--set smtp.enabled=true \
--set smtp.user=<yyyyyyyyyyyyyyyy> \
--set smtp.password=<zzzzzzzzzzzzzzzzzzzz> \
--set smtp.host=email-smtp.eu-central-1.amazonaws.com:587 \
--set smtp.fromAddress=<myemail>@gmail.com \
--set smtp.skipVerify=false \
--namespace jenkins
```

## Automated deployment using Jenkins
The Git repository includes a Jenkinsfile that defines a straightforward pipeline. This pipeline is triggered automatically every time changes are pushed to the GitHub repository. A webhook is configured to establish this connection between GitHub and Jenkins, ensuring that the pipeline executes seamlessly with each update.
Detailed Jenkins configuration was described in previous tasks.

## Grafana default user and password
In order to get the admin credentials, you just need to do this:
```
Get the admin credentials:
  echo "User: admin"
  echo "Password: $(kubectl get secret grafana-admi    --namespace jenkins -o jsonpath="{.data.GF_SECURITY_ADMIN_PASSWORD}" | base64 -d)"

```
Best option is to keep Grafana password as well as SMTP credentials in Jenkins Secrets and use it in Jenkins Pipeline as a variable:
```
        stage('Deploy Application to K3S using Helm') {
            steps {
                container('helm') {
                    withCredentials([
                        string(credentialsId: 'GRAFANA_ADMIN_PASSWORD', variable: 'GRAFANA_ADMIN_PASSWORD'),
                        string(credentialsId: 'SMTP_USER', variable: 'SMTP_USER'),
                        string(credentialsId: 'SMTP_PASSWORD', variable: 'SMTP_PASSWORD'),
                        string(credentialsId: 'SMTP_HOST', variable: 'SMTP_HOST'),
                        string(credentialsId: 'SMTP_EMAIL', variable: 'SMTP_EMAIL')
                    ]) {
                        sh """
                        helm repo add bitnami https://charts.bitnami.com/bitnami
                        helm repo update
                        helm upgrade --install grafana bitnami/grafana \\
                        --set service.type=NodePort \\
                        --set service.nodePorts.grafana=${GRAFANA_PORT} \\
                        --set admin.password=${GRAFANA_ADMIN_PASSWORD} \\
                        --set smtp.enabled=true \\
                        --set smtp.user=${SMTP_USER} \\
                        --set smtp.password=${SMTP_PASSWORD} \\
                        --set smtp.host=${SMTP_HOST} \\
                        --set smtp.fromAddress=${SMTP_EMAIL} \\
                        --set smtp.skipVerify=false \\
                        --namespace ${K3S_NAMESPACE}
                        """
                    }
                }
            }
        }
```

## Example of Alert configuration
<img width="1392" alt="Screenshot 2024-12-13 at 16 58 53" src="https://github.com/user-attachments/assets/7a956d4d-6da6-4b05-99b1-8c98f75cf1db" />

## Stress testing
### In order to overload CPU using default OS tools you can do this:
```
(reverse-i-search)`': ^C
ec2-user@ip-10-0-2-10:~> yes > /dev/null
^C
ec2-user@ip-10-0-2-10:~> 
```
### In order to overload RAM using default OS tools you can do this:
```
# Allocate 100 MB of RAM
dd if=/dev/zero of=/dev/shm/stress_test_$RANDOM bs=100M count=1
# Delete dummy RAM allocations
rm /dev/shm/stress_test_*
```
### Here is a DashBoard, showing these tricks effect:
<img width="1392" alt="Screenshot 2024-12-13 at 17 00 02" src="https://github.com/user-attachments/assets/5da995c2-5d41-4e1b-b98d-051a03a52987" />
### Here is what you have in your email inbox:
<img width="1196" alt="Screenshot 2024-12-13 at 17 01 26" src="https://github.com/user-attachments/assets/5400414a-b8b0-45a5-b059-dfc525a0b775" />



