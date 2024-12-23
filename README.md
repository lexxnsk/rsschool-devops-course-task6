# The RS School - AWS DevOps Course. Project Documentation. Task 6.
---
Dear Reviewer.

~~I kindly ask for your understanding and a brief extension to finalize my repository review. Due to unforeseen and urgent laptop issues, I was unable to dedicate the necessary time this weekend and finalize everything.
So far, I’ve maintained nearly maximum points, and I’m committed to delivering high-quality work. I would greatly appreciate it if the review could be postponed until the end of this week to allow me to complete the tasks to the best of my ability.
Great thanks in advance for your understanding.~~

**UPDATE:  
The task is complete. Thank you for granting me extra time to finish it. I truly appreciate it.  
You can review it now.  
~~Everything is done except for the SonarQube check.  
I’ve deducted 5 points for this, making the current total score 95/100.  
If additional time is provided, I might include the SonarQube check as well.~~  
**Everything is done, including the SonarQube check, resulting in a score of 100/100**
---

This repository contains a custom application - [telegram bot](screenshots/bot_qr_code.jpg) and it's helm chart for deployment, as well as Jenkins Pipeline.
~~I've hadcoded all API keys, because it is not a purpose of this task to make it secure.
Don't worry, at the moment you read this, all API keys are deleted already.
In production, of course, you need to use secrets.~~  
**All API keys are moved to secrets.**  
## Bot testing
<p align="center">
<img src="screenshots/bot_qr_code.jpg" width="500" />  
 </p>
You're welcome to play a bit with this bot.  
If it doesn't reply, it means, I've switched off the K3S node to save some money. If you really want - ping me and I will switch it on.
Here is how it should look like:
<p align="center">
<img src="screenshots/bot_in_action.jpg" width="500" />  
 </p>

## Manual deployment using local Docker
- docker build -t tristaprogrammista-bot .
- docker run -d --name tristaprogrammista-bot tristaprogrammista-bot
```
amyslivets@MacBook-Air-Alex rsschool-devops-course-task6 % docker build -t tristaprogrammista-bot .                          

[+] Building 5.8s (10/10) FINISHED                                                                                                                         docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                                                                       0.0s
 => => transferring dockerfile: 625B                                                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.13-slim                                                                                                        0.7s
 => [internal] load .dockerignore                                                                                                                                          0.0s
 => => transferring context: 2B                                                                                                                                            0.0s
 => [1/5] FROM docker.io/library/python:3.13-slim@sha256:4efa69bf17cfbd83a9942e60e2642335c3b397448e00410063a0421f9727c4c4                                                  0.0s
 => [internal] load build context                                                                                                                                          0.0s
 => => transferring context: 1.75kB                                                                                                                                        0.0s
 => CACHED [2/5] WORKDIR /app                                                                                                                                              0.0s
 => CACHED [3/5] COPY requirements.txt ./                                                                                                                                  0.0s
 => [4/5] COPY tristaprogrammista_bot.py ./                                                                                                                                0.0s
 => [5/5] RUN pip install --no-cache-dir -r requirements.txt                                                                                                               4.9s
 => exporting to image                                                                                                                                                     0.1s 
 => => exporting layers                                                                                                                                                    0.1s 
 => => writing image sha256:32f59abaca95cd75d1da0dfe17283555c07d8cfc5822761a1198c42bc2dd3fd2                                                                               0.0s 
 => => naming to docker.io/library/tristaprogrammista-bot                                                                                                                  0.0s 
                                                                                                                                                                                
View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/nz3a01dszhzac0nxt2pmago92                                                                      

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview 
amyslivets@MacBook-Air-Alex rsschool-devops-course-task6 % docker run -d --name tristaprogrammista-bot tristaprogrammista-bot

adda9874075b15017110466659cd59a8aa7bd8e0ea4e5ec805e1317c33086a23
amyslivets@MacBook-Air-Alex rsschool-devops-course-task6 % docker ps                                          
CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS         PORTS     NAMES
adda9874075b   tristaprogrammista-bot   "python tristaprogra…"   5 seconds ago   Up 4 seconds             tristaprogrammista-bot
amyslivets@MacBook-Air-Alex rsschool-devops-course-task6 % 
```
## Manual deployment using Helm Chart
- helm upgrade --install tristaprogrammista -n tristaprogrammista helm-charts/tristaprogrammista/
```
tristaprogrammista_botamyslivets@MacBook-Air-Alex rsschool-devops-course-task6 % helm list -A
NAME                    NAMESPACE               REVISION        UPDATED                                 STATUS          CHART                               APP VERSION
jenkins                 jenkins                 15              2024-11-22 14:34:27.796137 +0100 CET    deployed        jenkins-5.7.12                      2.479.1    
traefik                 kube-system             1               2024-11-03 12:30:33.156819527 +0000 UTC deployed        traefik-27.0.201+up27.0.2           v2.11.10   
traefik-crd             kube-system             1               2024-11-03 12:30:30.685130472 +0000 UTC deployed        traefik-crd-27.0.201+up27.0.2       v2.11.10   
tristaprogrammista      tristaprogrammista      3               2024-11-22 15:48:15.499506 +0100 CET    deployed        tristaprogrammista-0.1.0            1.16.0     
wordpress               wordpress               3               2024-11-09 17:36:57.991983249 +0000 UTC deployed        wordpress-0.1.0                     latest     
```

## ECR storage
<p align="center">
<img src="screenshots/awc_ecr.png" width="800" />  
</p>  

## Successful Pipe, generated by Jenkins Blue Ocean Plugin, including manual trigger
<p align="center">
<img src="screenshots/successful_pipe_with_sonar.png" width="800" />  
 </p>
<p align="center"> 
<img src="screenshots/manual_trigger.png" width="800" />  
</p>

## Notifications
<p align="center"> 
<img src="screenshots/notification_system.png" width="800" />  
 </p>
