# The RS School - AWS DevOps Course. Project Documentation. Task 8.
---

This repository branch contains a Jenkins Pipeline along with the required configuration adjustments to automate the deployment of Grafana, a multi-platform open source analytics and interactive visualization web application.

## Manual deployment using Helm
The provided code snippet demonstrates how to deploy Grafana in a Kubernetes cluster using Helm, a package manager for Kubernetes. It involves adding the Bitnami Helm repository, updating the repository index, and using the helm upgrade --install command to deploy the grafana chart.
- helm repo add bitnami https://charts.bitnami.com/bitnami
- helm repo update
- helm upgrade --install grafana bitnami/grafana \
    --set service.type=NodePort \
    --set service.nodePorts.grafana=32003

## Granting necessary permissions to Jenkins
To ensure the successful execution of the Jenkins pipeline, we need to grant the necessary permissions to Jenkins.
- kubectl apply -f jenkins-role.yaml

## Automated deployment using Jenkins
The Git repository includes a Jenkinsfile that defines a straightforward pipeline. This pipeline is triggered automatically every time changes are pushed to the GitHub repository. A webhook is configured to establish this connection between GitHub and Jenkins, ensuring that the pipeline executes seamlessly with each update.
Detailed Jenkins configuration was described in previous tasks.

## Access via Internet
An NGINX reverse proxy with TLS certificates is deployed on the Bastion host to ensure secure and encrypted access to the [Grafana Web UI](https://grafana.rss.myslivets.ru/). This setup safeguards communication by routing traffic through HTTPS, enhancing security and accessibility.
Here is an example of related NGINX proxy config:
```
server {

    server_name grafana.rss.myslivets.ru;

    location / {
        proxy_pass http://10.0.2.10:32003;  # Forward requests to the Grafana service
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/grafana.rss.myslivets.ru/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/grafana.rss.myslivets.ru/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


}
server {
    if ($host = grafana.rss.myslivets.ru) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name grafana.rss.myslivets.ru;
    return 404; # managed by Certbot


}

```

## HTTPS (TLS certificate deployment)
The certbot tool is used to create the certificate using Let's Encrypt service and deploy it into NGINX config

```
ubuntu@ip-10-0-0-252:~$ sudo apt-get install certbot python3-certbot-nginx
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
certbot is already the newest version (2.9.0-1).
python3-certbot-nginx is already the newest version (2.9.0-1).
0 upgraded, 0 newly installed, 0 to remove and 28 not upgraded.
ubuntu@ip-10-0-0-252:~$ 
ubuntu@ip-10-0-0-252:~$ sudo certbot --nginx -d grafana.rss.myslivets.ru
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Requesting a certificate for grafana.rss.myslivets.ru

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/grafana.rss.myslivets.ru/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/grafana.rss.myslivets.ru/privkey.pem
This certificate expires on 2025-03-02.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

Deploying certificate
Successfully deployed certificate for grafana.rss.myslivets.ru to /etc/nginx/sites-enabled/default
Congratulations! You have successfully enabled HTTPS on https://grafana.rss.myslivets.ru

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

```

## Grafana default user and password.
In order to get the admin credentials, you just need to do this:
```
2. Get the admin credentials:

    echo "User: admin"
    echo "Password: $(kubectl get secret grafana-admin --namespace jenkins -o jsonpath="{.data.GF_SECURITY_ADMIN_PASSWORD}" | base64 -d)"

```

## Problem met
During this task, I encountered an issue with a failing Jenkins pod when running a pipeline, which was caused by insufficient disk space. The problem was resolved by increasing the disk space and extending the filesystem.
```
aws ec2 modify-volume --volume-id vol-0e218ffe06c8e6c12 --size 30
sudo growpart /dev/nvme0n1 3
sudo xfs_growfs /dev/nvme0n1p3
ec2-user@ip-10-0-2-10:~> df -h /dev/nvme0n1p3
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p3   30G  8.2G   22G  28% /
```
